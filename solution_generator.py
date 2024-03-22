from loader import load_grid,save_grid
from collections import deque
from graph import RoomGraph
from copy import deepcopy
import random

'''
TABLES c = chair t = table

xxxx
cttc = 1
xxxx 

xxxx
cttc = 2
cttc
xxxx

xxcxx
ctttc = 3  
ctttc
ctttc
xxcxx

 ccc
xtttx
ctttc
xtttx
 ccc
'''
NODES_TO_TABLE = {
    (1,'h'):set([(0,0),(0,1)]),
    (1,'v'):set([(0,0),(1,0)]),
    (2,'h'):set([(0,0),(0,1),(1,0),(1,1)]),
    (2,'v'):set([(0,0),(1,0),(0,1),(1,1)]),
    (3,'h'):set([(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]),
    (3,'v'):set([(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]),
}
NODES_TO_CHAIR = {
    (1,'h'):set([(0,-1),(0,2)]),
    (1,'v'):set([(-1,0),(2,0)]),
    (2,'h'):set([(0,-1),(0,2),(1,-1),(1,2)]),
    (2,'v'):set([(-1,0),(2,0),(-1,1),(2,1)]),
    (3,'h'):set([(0,-1),(0,3),(1,-1),(1,3),(2,-1),(2,3),(-1,1),(3,1)]),
    (3,'v'):set([(-1,0),(-1,1),(-1,2),(3,0),(3,1),(3,2),(1,-1),(1,3)]),
}
NODES_TO_RESTRICTED = {
    (1,'h'):set([(-1,-1),(-1,0),(-1,1),(-1,2),(1,-1),(1,0),(1,1),(1,2)]),
    (1,'v'):set([(-1,-1),(0,-1),(1,-1),(2,-1),(-1,1),(0,1),(1,1),(2,1)]),
    (2,'h'):set([(-1,-1),(-1,0),(-1,1),(-1,2),(2,-1),(2,0),(2,1),(2,2)]),
    (2,'v'):set([(-1,-1),(0,-1),(1,-1),(2,-1),(-1,2),(0,2),(1,2),(2,2)]),
    (3,'h'):set([(-1,-1),(-1,0),(-1,2),(-1,3),(3,-1),(3,0),(3,1),(3,2)]),
    (3,'v'):set([(-1,-1),(0,-1),(2,-1),(3,-1),(-1,3),(0,3),(2,3),(3,3)]),
}
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

def select_table_placment(roomGraph:RoomGraph,table_type:int,orientation:str = None):
    if orientation is None:
        orientation = random.choice(['h','v'])
    if orientation != 'h' and orientation != 'v':
        return None
    number_of_tries = 0
    while True:
        number_of_tries += 1
        if number_of_tries > 100:
            print('could not place table ',table_type,orientation,' after 100 tries')
            return roomGraph
        can_place = True
        placement = random.choice(list(roomGraph.graph.keys()))
        for node in NODES_TO_TABLE[(table_type,orientation)]:
            if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.tables:
                can_place = False
                break
            if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.chairs:
                can_place = False
                break
            if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.restricted:
                can_place = False
                break
            if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.walls:
                can_place = False
                break
        for node in NODES_TO_CHAIR[(table_type,orientation)]:
            if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.tables:
                can_place = False
                break
            if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.chairs:
                can_place = False
                break
            if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.restricted:
                can_place = False
                break
            if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.walls:
                can_place = False
                break
        for node in NODES_TO_RESTRICTED[(table_type,orientation)]:
            if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.tables:
                can_place = False
                break
            if (placement[0]+node[0],placement[1]+node[1]) in roomGraph.chairs:
                can_place = False
                break
        if can_place:
            new_roomGraph = deepcopy(roomGraph)
            for node in NODES_TO_TABLE[(table_type,orientation)]:
                new_roomGraph.tables.add((placement[0]+node[0],placement[1]+node[1]))
                new_roomGraph.graph[(placement[0]+node[0],placement[1]+node[1])] = []
            for node in NODES_TO_CHAIR[(table_type,orientation)]:
                new_roomGraph.chairs.add((placement[0]+node[0],placement[1]+node[1]))
            for node in NODES_TO_RESTRICTED[(table_type,orientation)]:
                new_roomGraph.restricted.add((placement[0]+node[0],placement[1]+node[1]))
            for door in new_roomGraph.doors:
                distances = BFS(new_roomGraph.graph,door)
                for chair in new_roomGraph.chairs:
                    if distances[chair] == float('inf'):
                        print('for placment: ',placement,'no path to: ',chair)
                        can_place = False
        
        if can_place:
            roomGraph = new_roomGraph
            return roomGraph
        


roomGraph = load_grid('grids/grid1')

# print('walls',roomGraph.walls)
# print('doors',roomGraph.doors)
# print('restricted',roomGraph.restricted)
# print(roomGraph.graph)
for i in range(0,10):
    roomGraph = select_table_placment(roomGraph,1)
    roomGraph = select_table_placment(roomGraph,2)
    roomGraph = select_table_placment(roomGraph,3)
save_grid(roomGraph,'grids/grid_test')