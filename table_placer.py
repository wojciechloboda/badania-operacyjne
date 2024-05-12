from collections import deque
from copy import deepcopy
from CONST import NODES_TO_CHAIR, NODES_TO_RESTRICTED, NODES_TO_TABLE
from graph import RoomGraph

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

def does_paths_to_doors_exist(roomGraph:RoomGraph, placement):
    #TODO - do we want paths to all doors from all chairs or just to one door?
    for door in roomGraph.doors:
        distances = BFS(roomGraph.graph,door)
        for chair in roomGraph.chairs:
            if distances[chair] == float('inf'):
                # print('for placment: ',placement,'no path to: ',chair)
                return False
    return True

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
    new_roomGraph.table_list.append({"type":table_type, "orientation":orientation, "place":placement})
    for node in NODES_TO_TABLE[(table_type,orientation)]:
        new_roomGraph.tables.add((placement[0]+node[0],placement[1]+node[1]))
        new_roomGraph.graph[(placement[0]+node[0],placement[1]+node[1])] = []
    for node in NODES_TO_CHAIR[(table_type,orientation)]:
        new_roomGraph.chairs.add((placement[0]+node[0],placement[1]+node[1]))
    for node in NODES_TO_RESTRICTED[(table_type,orientation)]:
        new_roomGraph.restricted.add((placement[0]+node[0],placement[1]+node[1]))
    return new_roomGraph

def remove_table(roomGraph:RoomGraph, id:int):
    table_type=roomGraph.table_list[id]['type']
    orientation=roomGraph.table_list[id]['orientation']
    placement=roomGraph.table_list[id]['place']
    for node in NODES_TO_TABLE[(table_type,orientation)]:
        roomGraph.tables.remove((placement[0]+node[0],placement[1]+node[1]))
        #roomGraph.graph[(placement[0]+node[0],placement[1]+node[1])] = [] - HOW TO REVERT THIS??
    for node in NODES_TO_CHAIR[(table_type,orientation)]:
        roomGraph.chairs.remove((placement[0]+node[0],placement[1]+node[1]))
    for node in NODES_TO_RESTRICTED[(table_type,orientation)]:
        roomGraph.restricted.remove((placement[0]+node[0],placement[1]+node[1]))
    roomGraph.table_list.pop(id)
    return roomGraph
