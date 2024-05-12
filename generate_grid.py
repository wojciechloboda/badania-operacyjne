
import random

def samplegrid(w, h, n):
    return [divmod(i, w) for i in random.sample(range(w * h), n)]

def generate_grid(N, M, proc, filename):
    grid = [[' ' for _ in range(M)] for _ in range(N) ]
    for x, y in samplegrid(M, N, int((N - 2) * (M - 2) * proc)):
        grid[x][y] = '#'

    for i in range(M):
        grid[0][i] = '#'
        grid[-1][i] = '#'

    for i in range(N):
        grid[i][0] = '#'
        grid[i][-1] = '#'

    grid[0][1] = '@'

    with open(filename, 'w') as file:
        for row in grid:
            file.write(''.join(row) + '\n')



if __name__ == "__main__":
    generate_grid(30, 20, 0.90, 'new_rand')

