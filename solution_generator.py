from loader import load_grid,save_grid, save_table_list
from graph import RoomGraph
import random
from numpy.random import permutation
from table_placer import does_paths_to_doors_exist, place_table, possible_to_place

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

if __name__=="__main__":
    for j in range (10):
        print(f"Generating grid numer {j}")
        roomGraph = load_grid('grids_empty/grid1')
        for i in range(0,10):
            roomGraph = select_table_placment(roomGraph,1)
            roomGraph = select_table_placment(roomGraph,2)
            roomGraph = select_table_placment(roomGraph,3)
        save_grid(roomGraph,f'grids_solutions/sol_grid{j}')
        save_table_list(roomGraph.table_list,f'grids_solutions/sol_tlist{j}')