
import random

def samplegrid(w, h, n):
    return [divmod(i, h) for i in random.sample(range(w * h), n)]

if __name__ == "__main__":
    N = 10
    M = 10
    grid = [[' ' for _ in range(M)] for _ in range(N) ]

    for x, y in samplegrid(M, N, N * M // 8):
        grid[x][y] = '#'

    for i in range(N):
        grid[0][i] = '#'
        grid[-1][i] = '#'

    for i in range(M):
        grid[i][0] = '#'
        grid[i][-1] = '#'

    grid[0][1] = '@'

    with open('random_grid10', 'w') as file:
        for row in grid:
            file.write(''.join(row) + '\n')

