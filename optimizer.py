
def run_ga(pop_size, generations, max_risk, hedef):
    import random
    import numpy as np

    def fitness(route):
        if hedef == "Minimum Mesafe":
            return sum(abs(route[i] - route[i+1]) for i in range(len(route)-1))
        elif hedef == "Minimum Süre":
            return sum((abs(route[i] - route[i+1])*2) for i in range(len(route)-1))
        elif hedef == "Minimum Risk":
            return sum((route[i]+route[i+1])%3 for i in range(len(route)-1))
        elif hedef == "Maksimum Ortalama Hız":
            dist = sum(abs(route[i] - route[i+1]) for i in range(len(route)-1))
            time = sum((abs(route[i] - route[i+1])*2) for i in range(len(route)-1))
            return -dist/(time/60) if time > 0 else float('inf')
        return 999999

    cities = list(range(8))
    def selection(pop): return min(random.sample(pop, 3), key=fitness)
    def crossover(p1, p2): return p1[:4] + p2[4:]
    def mutate(route): pass
    pop = [random.sample(cities, len(cities)) for _ in range(pop_size)]
    for _ in range(generations): pop = [crossover(selection(pop), selection(pop)) for _ in pop]
    best = min(pop, key=fitness)
    d = sum(abs(best[i] - best[i+1]) for i in range(len(best)-1))
    t = d * 2
    r = sum((best[i]+best[i+1])%3 for i in range(len(best)-1)) * 0.1
    return best, round(d,2), round(t,1), round(r,2), [{"from": "X", "to": "Y", "arrival": "08:00", "departure": "08:30"}]
