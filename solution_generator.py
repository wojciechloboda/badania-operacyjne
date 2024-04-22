from CONST import NODES_TO_TABLE, NODES_TO_CHAIR, NODES_TO_RESTRICTED
from loader import load_grid,save_grid
from collections import deque
from graph import RoomGraph
from copy import deepcopy
import random
from numpy.random import permutation

def BFS(graph,start):
    #Graph dict, key = (i,j), value = [(i1,j1),(i2,j2),...]
    #return dict, key = (i,j), value = distance
    queue = deque([start])
    distance = {}
    for key in graph.keys():
        distance[key] = float('inf')
    distance[start] = 0
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distance[neighbor] == float('inf'):
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return distance

def possible_to_place(roomGraph:RoomGraph, table_type:int, orientation:str, placement):
    # placement = random.choice(list(roomGraph.graph.keys()))
    for node in NODES_TO_TABLE[(table_type,orientation)]:
        if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.tables:
            return False
        if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.chairs:
            return False
        if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.restricted:
            return False
        if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.walls:
            return False
    for node in NODES_TO_CHAIR[(table_type,orientation)]:
        if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.tables:
            return False
        if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.chairs:
            return False
        if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.restricted:
            return False
        if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.walls:
            return False
    for node in NODES_TO_RESTRICTED[(table_type,orientation)]:
        if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.tables:
            return False
        if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.chairs:
            return False
    return True

def place_table(roomGraph:RoomGraph, table_type:int, orientation:str, placement):
    new_roomGraph = deepcopy(roomGraph)
    for node in NODES_TO_TABLE[(table_type,orientation)]:
        new_roomGraph.tables.add((placement[0]+node[0],placement[1]+node[1]))
        new_roomGraph.graph[(placement[0]+node[0],placement[1]+node[1])] = []
    for node in NODES_TO_CHAIR[(table_type,orientation)]:
        new_roomGraph.chairs.add((placement[0]+node[0],placement[1]+node[1]))
    for node in NODES_TO_RESTRICTED[(table_type,orientation)]:
        new_roomGraph.restricted.add((placement[0]+node[0],placement[1]+node[1]))
    return new_roomGraph

def does_paths_to_doors_exist(roomGraph:RoomGraph, placement):
    #TODO - do we want paths to all doors from all chairs or just to one door?
    for door in roomGraph.doors:
        distances = BFS(roomGraph.graph,door)
        for chair in roomGraph.chairs:
            if distances[chair] == float('inf'):
                print('for placment: ',placement,'no path to: ',chair)
                return False
    return True

def select_table_placment(roomGraph:RoomGraph,table_type:int,orientation:str = None):
    if orientation is None:
        orientation = random.choice(['h','v'])
    if orientation != 'h' and orientation != 'v':
        return None
    number_of_tries = 0
    perm = permutation(list(roomGraph.graph.keys()))
    for placement in perm:
        can_place=possible_to_place(roomGraph, table_type, orientation, placement)
        if can_place:
            new_roomGraph=place_table(roomGraph, table_type, orientation, placement)
            if(does_paths_to_doors_exist(new_roomGraph, placement)):
                return new_roomGraph
    print('could not place table')
    return roomGraph


# print('walls',roomGraph.walls)
# print('doors',roomGraph.doors)
# print('restricted',roomGraph.restricted)
# print(roomGraph.graph)

for j in range (10):
    print(f"Generating grid numer {j}")
    roomGraph = load_grid('grids_empty/grid1')
    for i in range(0,10):
        roomGraph = select_table_placment(roomGraph,1)
        roomGraph = select_table_placment(roomGraph,2)
        roomGraph = select_table_placment(roomGraph,3)
    save_grid(roomGraph,f'grids_solutions/sol{j}')