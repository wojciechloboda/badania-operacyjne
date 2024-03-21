
DOOR = '@'
WALL = '#'
EMPTY = ' '

def get_door(grid):
    for i in range(len(grid)):
        idx = grid[i].find(DOOR) 
        if idx != -1:
            return (i, idx)
    return None

def in_grid(i, j, grid):
    return i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0])

def get_adj(i, j, grid):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    res = []
    for di, dj in dirs:
        if in_grid(i + di, j + dj, grid) and grid[i + di][j + dj] == EMPTY:
            res.append((i + di, j + dj))
    return res

def load_grid(path):
    with open(path) as f:
        grid = f.read().split('\n')
    n = len(grid)
    m = len(grid[0])
    graph = dict()
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if grid[i][j] != WALL:
                graph[(i, j)] = get_adj(i, j, grid)

    door = get_door(grid)
    if door is not None:
        i, j = door
        graph[door] = get_adj(i, j, grid)

    return door, graph

print(load_grid('grids/grid2'))