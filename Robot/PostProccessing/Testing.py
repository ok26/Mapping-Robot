import numpy as np
import matplotlib.pyplot as plt
from math import tan, pi
import time

room = np.loadtxt("from mac/Robot/SavedRoom.txt")
room = np.rot90(room)
room[np.where(room==2)] = 0

start = time.time()

indexes = list()


def remove_island(coord):
    i = coord[0]
    j = coord[1]

    if i < 0 or i >= len(room) or j < 0 or j >= len(room[0]) or\
            to_remove[i][j] is True or room[i][j] == 0:
        return 0

    to_remove[i][j] = True

    for r in range(i-1, i+2, 1):
        if r != i:
                remove_island((r, j))
    for c in range(j-1, j+2, 1):
        if c != j:
            remove_island((i, c))


def count_houses(mat, visited, i, j):
    if i < 0 or i >= len(mat) or j < 0 or j >= len(mat[0]) or\
            visited[i][j] is True or mat[i][j] == 0:
        return 0

    visited[i][j] = True
    cnt = 1
   
    for r in range(i-1, i+2, 1):
        if r != i:
                cnt += count_houses(mat, visited, r, j)
    for c in range(j-1, j+2, 1):
        if c != j:
            cnt += count_houses(mat, visited, i, c)
    return cnt


def island_count(mat):
    houses = list()
    clusters = 0
    row = len(mat)
    col = len(mat[0])
    visited = [[False for i in range(col)] for j in range(row)]

    for i in range(row):
        for j in range(col):
            if mat[i][j] == 1 and visited[i][j] is False:

                indexes.append((i, j))

                clusters += 1
                h = count_houses(mat, visited, i, j)
                houses.append(h)
    return houses


def check_diag(i,j):
    for ang in range(0,89,5):
        x = 1
        y = 0
        lastY = 0
        first = True
        signY = -1
        signX = 1
        while True:
            y = int(round(tan(ang*pi/180)*x,0))
            if i+y*signY < len(room) and i+y*signY >= 0 and j+x*signX < len(room[0]) and j+x*signX >= 0:
                if abs(y-lastY) > 1:
                    if signX > 0:
                        room[i+y*signY:i+lastY*signY,j+signX*(x-1)] = 2
                    else:
                        room[i+lastY*signY:i+y*signY,j+signX*(x-1)] = 2
                    print(lastY*signY,y*signY,signX*(x-1))
                else:
                    room[i+y*signY,j+x*signX] = 2
                x += 1
                lastY = y
            else:
                if first:
                    first = False
                    x = 0
                    lastY = 0
                    signY = -signY
                    signX = -signX
                else:
                    break
    #return count





island_size = island_count(room)
to_remove = [[False for i in range(len(room))] for j in range(len(room[0]))]
for i in range(len(island_size)):
    if island_size[i] <= 50:
        remove_island(indexes[i])

room[np.where(to_remove)] = 0
del to_remove

checked = [[False for i in range(len(room))] for j in range(len(room[0]))]

for i in range(len(room)):
    for j in range(len(room[0])):
        if i < 0 or i >= len(room) or j < 0 or j >= len(room[0]) or\
            checked[i][j] is True or room[i][j] == 0:
            continue

check_diag(237,150)




room[237,150] = 2


print(time.time()-start)

plt.imshow(room)

plt.show()