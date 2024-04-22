from CONST import NODES
from graph import RoomGraph
import random
from numpy.random import permutation
from time import time
from loader import load_grid, load_solution, save_grid
from solution_generator import does_paths_to_doors_exist
from table_placer import place_table, possible_to_place, remove_table

def cross(mother:RoomGraph, father: RoomGraph, empty_graph: RoomGraph):
    child=empty_graph
    n_mother_genes=len(mother.table_list) if len(mother.table_list)<=3 else random.randrange(1, len(mother.table_list)-1)
    print(f"mother genes: {n_mother_genes/len(mother.table_list)}")
    mother_genes= random.sample(mother.table_list, n_mother_genes)
    for gene in mother_genes:
        child=place_table(child, gene["type"], gene["orientation"], gene["place"])
    for gene in father.table_list:
        if(possible_to_place(child, gene["type"], gene["orientation"], gene["place"])):
            child=place_table(child, gene["type"], gene["orientation"], gene["place"])
    return child

def mutate(child: RoomGraph):
    mutation_type=random.random()
    if mutation_type <=0.2: #MUTATION TYPE -1
        print("mutatution type -1: removing 1 table")
        table_id_to_remove=random.randint(0, len(child.table_list)-1)
        remove_table(child, table_id_to_remove)
    elif mutation_type <=0.8: #MUTATION TYPE 1
        print("mutatution type 1: trying to add from 1 to 3 tables")
        max_to_place=random.randint(1, 3)
        placed_cnt=0
        perm = permutation(list(child.graph.keys()))
        for table_type, orientation in NODES:
            for placement in perm:
                can_place=possible_to_place(child, table_type, orientation, placement)
                if can_place:
                    new_child=place_table(child, table_type, orientation, placement)
                    if(does_paths_to_doors_exist(new_child, placement)):
                        child=new_child
                        placed_cnt+=1
                        print(f"placed {placed_cnt} table")
                        if placed_cnt>=max_to_place: return child
    else: #MUTATION TYPE 0
        print("mutatution type 0: no mutation")
    return child

if __name__=='__main__':
    random.seed(time())
    graph1 = load_solution('grids_solutions/sol_grid0', 'grids_solutions/sol_tlist0')
    graph2 = load_solution('grids_solutions/sol_grid1', 'grids_solutions/sol_tlist1')
    child_graph=load_grid('grids_empty/grid1')
    child_graph=cross(graph1, graph2, child_graph)
    child_graph=mutate(child_graph)
    save_grid(child_graph,f'grids_crossed/child_0_1')