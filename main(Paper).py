import random
import math

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
# Distance
# ---------------------------
def distance(a, b):
    return int(round(math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)))


def total_distance(route, cities):
    return sum(distance(cities[route[i]], cities[route[(i+1) % len(route)]])
               for i in range(len(route)))


# ---------------------------
# NLSA
# ---------------------------
def NLSA(route, cities):
    best = route[:]
    best_dist = total_distance(best, cities)

    improved = True
    while improved:
        improved = False
        for i in range(len(route) - 1):
            new_route = best[:]
            new_route[i+1:] = reversed(new_route[i+1:])

            new_dist = total_distance(new_route, cities)

            if new_dist < best_dist:
                best = new_route
                best_dist = new_dist
                improved = True
                break

    return best


# ---------------------------
# Crossover
# ---------------------------
def crossover(p1, p2, cities):
    n = len(p1)
    start = random.choice(p1)

    child = [start]
    visited = set(child)

    current = start
    while len(child) < n:
        idx1 = p1.index(current)
        idx2 = p2.index(current)

        n1 = [p1[(idx1-1)%n], p1[(idx1+1)%n]]
        n2 = [p2[(idx2-1)%n], p2[(idx2+1)%n]]

        common = [c for c in n1 if c in n2 and c not in visited]

        if common:
            next_city = common[0]
        else:
            remaining = [c for c in p1 if c not in visited]
            next_city = min(remaining, key=lambda c: distance(cities[current], cities[c]))

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
# HGA
# ---------------------------
def HGA(cities, generations=1000, pop_size=100):
    population = [random.sample(range(len(cities)), len(cities)) for _ in range(pop_size)]
    population = [NLSA(ind, cities) for ind in population]

    for gen in range(generations):
        population.sort(key=lambda r: total_distance(r, cities))

        p1 = population[0]
        p2 = random.choice(population)

        child = crossover(p1, p2, cities)
        child = NLSA(child, cities)
        child = mutate(child)

        if child not in population:
            population[-1] = child

        if gen % 50 == 0:
            print(f"Gen {gen}: Best Distance = {total_distance(population[0], cities):.2f}")

    return population[0]


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    filename = input("Enter dataset file (e.g., berlin52.tsp): ")

    cities = load_tsp(filename)
    print(f"Loaded {len(cities)} cities.")

    best = HGA(cities)

    print("\nFinal Best Distance:", total_distance(best, cities))
    print("Best Route:", best)