from graph import RoomGraph
DOOR = '@'
WALL = '#'
EMPTY = ' '
TABLE = 'T'
CHAIR = 'C'

#TODO: add walls to the graph
def get_door(grid):
    doors = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == DOOR:
                doors.add((i, j))
    if len(doors) ==0:
        return None
    return doors

def in_grid(i, j, grid):
    return i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0])

def get_adj(i, j, grid):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    res = []
    for di, dj in dirs:
        if in_grid(i + di, j + dj, grid) and (grid[i + di][j + dj] == EMPTY or grid[i + di][j + dj] == DOOR):
            res.append((i + di, j + dj))
    return res

def load_grid(path):
    with open(path) as f:
        grid = f.read().split('\n')
    n = len(grid)
    m = len(grid[0])
    roomGraph = RoomGraph()
    for i in range(0, n):
        for j in range(0, m):
            if grid[i][j] != WALL:
                roomGraph.graph[(i, j)] = get_adj(i, j, grid)
            else:
                roomGraph.walls.add((i, j))

    roomGraph.doors = get_door(grid)
    if roomGraph.doors is None:
        return roomGraph
    for door in roomGraph.doors:
        i, j = door
        roomGraph.graph[door] = get_adj(i, j, grid)
        roomGraph.restricted.add(door)

    return roomGraph

def save_grid(roomGraph, path):
    min_y = min([x[0] for x in roomGraph.walls])
    min_x = min([x[1] for x in roomGraph.walls])
    max_y = max([x[0] for x in roomGraph.walls])
    max_x = max([x[1] for x in roomGraph.walls])
    grid = [[' ' for i in range(min_x, max_x + 1)] for j in range(min_y, max_y + 1)]
    for wall in roomGraph.walls:
        i, j = wall
        grid[i - min_y][j - min_x] = WALL
    for door in roomGraph.doors:
        i, j = door
        grid[i - min_y][j - min_x] = DOOR
    for table in roomGraph.tables:
        i, j = table
        grid[i - min_y][j - min_x] = TABLE
    for chair in roomGraph.chairs:
        i, j = chair
        grid[i - min_y][j - min_x] = CHAIR
    # for restricted in roomGraph.restricted:
    #     i, j = restricted
    #     grid[i - min_y][j - min_x] = 'x'
    with open(path, 'w') as f:
        for row in grid:
            f.write(''.join(row) + '\n')
