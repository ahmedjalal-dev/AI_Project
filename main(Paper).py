import random
import math
from concurrent.futures import ProcessPoolExecutor

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
# Distance calc
# ---------------------------
def total_distance(route, dist, n):
    total = 0
    for i in range(n - 1):
        total += dist[route[i]*n + route[i+1]]
    total += dist[route[-1]*n + route[0]]
    return total


# ---------------------------
# NLSA
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
# Parallel worker for init
# ---------------------------
def init_worker(args):
    n, dist = args
    r = random.sample(range(n), n)
    return NLSA(r, dist, n)


# ---------------------------
# Crossover (unchanged)
# ---------------------------
def crossover(p1, p2, dist, n):
    pos1 = {city: i for i, city in enumerate(p1)}
    pos2 = {city: i for i, city in enumerate(p2)}

    start = random.choice(p1)
    child = [start]
    visited = {start}
    current = start

    while len(child) < n:
        idx1 = pos1[current]
        idx2 = pos2[current]

        n1 = (p1[(idx1-1)%n], p1[(idx1+1)%n])
        n2 = (p2[(idx2-1)%n], p2[(idx2+1)%n])

        found = None
        for c in n1:
            if c in n2 and c not in visited:
                found = c
                break

        if found is not None:
            next_city = found
        else:
            best_city = None
            best_dist = 10**12
            for c in p1:
                if c not in visited:
                    d = dist[current*n + c]
                    if d < best_dist:
                        best_dist = d
                        best_city = c
            next_city = best_city

        child.append(next_city)
        visited.add(next_city)
        current = next_city

    return child


# ---------------------------
# Mutation
# ---------------------------
def mutate(route, rate=0.05):
    if random.random() < rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route


# ---------------------------
# HGA with parallelism
# ---------------------------
def HGA(cities, generations=1000, pop_size=100, workers=4):
    n = len(cities)
    dist = build_dist_matrix(cities)

    # ---- Parallel initialization ----
    with ProcessPoolExecutor(max_workers=workers) as executor:
        population = list(executor.map(init_worker, [(n, dist)] * pop_size))

    for gen in range(generations):
        population.sort(key=lambda x: x[1])

        p1 = population[0][0]
        p2 = random.choice(population)[0]

        child = crossover(p1, p2, dist, n)

        # occasional local search (parallelizable but keep sequential for stability)
        if gen % 5 == 0:
            child, d = NLSA(child, dist, n)
        else:
            d = total_distance(child, dist, n)

        child = mutate(child)
        d = total_distance(child, dist, n)

        population[-1] = (child, d)

        if gen % 50 == 0:
            print(f"Gen {gen}: Best Distance = {population[0][1]:.2f}")

    return population[0]


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    file = input("Enter dataset file (e.g., berlin52.tsp): ")
    cities = load_tsp(file)

    print(f"Loaded {len(cities)} cities.")

    best_route, best_dist = HGA(cities, workers=4)

    print("\nFinal Best Distance:", best_dist)
    print("Best Route:", best_route)