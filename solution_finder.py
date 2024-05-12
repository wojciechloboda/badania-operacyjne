from loader import load_grid, save_grid, save_table_list
from solution_generator import generate_solution
from copy import deepcopy
from solution_crosser import cross, mutate
import itertools
import random
from time import perf_counter
import asyncio

TABLE_SPECS = [(1, 5), (2, 5), (3, 5)]

def create_new(s1, s2, empty):
    new_graph = deepcopy(empty)
    new_graph = cross(s1, s2, new_graph)
    new_graph = mutate(new_graph)
    return new_graph


def find_solutions(graph, population_size, steps_count):
    population = [deepcopy(graph) for _ in range(population_size)]
    # print("generating initial setups...")
    for i in range(population_size):
        population[i] = generate_solution(population[i], TABLE_SPECS)

    # print("finding solutions...")
    stats = []
    pairs = list(itertools.combinations([i for i in range(population_size//2)], 2)) 

    population = sorted(population, key=lambda x: -1 * len(x.chairs))
    for s in range(steps_count):  
        # print(f"{s / steps_count * 100:.2f}%")
        start = perf_counter()

        random.shuffle(pairs) 
        # tasks = [create_new(population[idx1], population[idx2], graph) for idx1, idx2 in pairs[:population_size//2]]
        # new_graphs = await asyncio.gather(*tasks)
        # for i in range(population_size//2):
        #     population[population_size - 1 - i] = new_graphs[i]

        for i in range(population_size//2):
            new_graph = deepcopy(graph)
            idx1, idx2 = pairs[i]
            new_graph = cross(population[idx1], population[idx2], new_graph)
            new_graph = mutate(new_graph)
            population[population_size - 1 - i] = new_graph
        population = sorted(population, key=lambda x: -1 * len(x.chairs))

        end = perf_counter()
        time = end - start

        print(f"epoch {s + 1} took {time:.2f}s | best solution: {len(population[0].chairs)} chairs")
        stats.append({"best": population[0], "time": time})

    return stats




if __name__ == '__main__':
    grid = 'grids_empty/grid1'
    graph = load_grid(grid)
    stats = asyncio.run(find_solutions(graph, 10, 10, [(1, 5), (2, 5), (3, 5)]))
    print(stats)















