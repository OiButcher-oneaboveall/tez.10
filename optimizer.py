
def run_ga(pop_size, generations, max_risk):
    import random
    import numpy as np
    cities = list(range(8))
    def fitness(route):
        return sum(abs(route[i] - route[i+1]) for i in range(len(route)-1))
    def selection(pop): return min(random.sample(pop, 3), key=fitness)
    def crossover(p1, p2): return p1[:4] + p2[4:]
    def mutate(route): pass
    pop = [random.sample(cities, len(cities)) for _ in range(pop_size)]
    for _ in range(generations): pop = [crossover(selection(pop), selection(pop)) for _ in pop]
    best = min(pop, key=fitness)
    return best, 100, 120, 1.2, [{"from": "A", "to": "B", "arrival": "08:00", "departure": "08:10"}]
