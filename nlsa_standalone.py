import math
import random
import time

# ---------------------------
# Load TSPLIB
# ---------------------------
def load_tsp(filename):
    coords = []
    with open(filename, 'r') as f:
        start = False
        for line in f:
            if "NODE_COORD_SECTION" in line:
                start = True
                continue
            if "EOF" in line:
                break
            if start:
                parts = line.strip().split()
                coords.append((float(parts[1]), float(parts[2])))
    return coords

# ---------------------------
# Distance Matrix
# ---------------------------
def build_dist_matrix(cities):
    n = len(cities)
    dist = [0] * (n * n)
    for i in range(n):
        xi, yi = cities[i]
        for j in range(n):
            dx = xi - cities[j][0]
            dy = yi - cities[j][1]
            dist[i*n + j] = int(round(math.sqrt(dx*dx + dy*dy)))
    return dist

# ---------------------------
# Tour length
# ---------------------------
def total_distance(route, dist, n):
    total = 0
    for i in range(n - 1):
        total += dist[route[i]*n + route[i+1]]
    total += dist[route[-1]*n + route[0]]
    return total

# ---------------------------
# Nearest Neighbour Init
# ---------------------------
def nearest_neighbour(dist, n):
    visited = [False] * n
    route = [0]
    visited[0] = True
    for _ in range(n - 1):
        last = route[-1]
        best_next = -1
        best_d = float('inf')
        for j in range(n):
            if not visited[j] and dist[last*n + j] < best_d:
                best_d = dist[last*n + j]
                best_next = j
        route.append(best_next)
        visited[best_next] = True
    return route

# ---------------------------
# NLSA (same as paper impl)
# ---------------------------
def NLSA(route, dist, n, max_segment=40):
    best = route[:]
    best_dist = total_distance(best, dist, n)

    improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            a = best[i-1]
            b = best[i]
            upper = min(i + max_segment, n)
            for j in range(i + 1, upper):
                c = best[j]
                d = best[(j+1) % n]
                if dist[a*n + c] + dist[b*n + d] >= dist[a*n + b] + dist[c*n + d]:
                    continue
                new_route = best[:]
                new_route[i:j+1] = reversed(new_route[i:j+1])
                new_dist = total_distance(new_route, dist, n)
                if new_dist < best_dist:
                    best = new_route
                    best_dist = new_dist
                    improved = True
                    break
            if improved:
                break

    return best, best_dist

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    file = input("Enter dataset file (e.g., berlin52.tsp): ")
    cities = load_tsp(file)
    n = len(cities)
    print(f"Loaded {n} cities.")

    dist = build_dist_matrix(cities)

    # Start from nearest-neighbour tour (same quality init as paper)
    print("Building nearest-neighbour initial tour...")
    init_tour = nearest_neighbour(dist, n)
    init_dist = total_distance(init_tour, dist, n)
    print(f"Initial tour distance: {init_dist}")

    # Run NLSA once
    print("Running NLSA...")
    t0 = time.time()
    best_route, best_dist = NLSA(init_tour, dist, n)
    elapsed = time.time() - t0

    print(f"\nFinal Best Distance: {best_dist}")
    print(f"Time taken: {elapsed:.2f}s")
    print("Best Route:", best_route)
    input("\nPress any key to continue . . . ")
