import numpy as np
import matplotlib.pyplot as plt
from math import tan, pi
import time

room = np.loadtxt("Robot/SavedRoom.txt")
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
    

                        
def check_diag(i,j, ang):
    lines = np.zeros((300,300))
   
    if ang == 90:
        lines[0:i,j] = True
        lines[i:len(room),j] = True
        return lines
    if ang > 90:
        ang = 90-(ang-90)
        rond = 2
        signY = 1
        signX = 1
    else:
        rond = 0
        signY = -1
        signX = 1

    x = 1
    y = 0
    lastY = 0
        
    while True:
        y = int(round(tan(ang*pi/180)*x,0))
        if i+y*signY < len(room) and i+y*signY >= 0 and j+x*signX < len(room[0]) and j+x*signX >= 0:
            
            if abs(y-lastY) > 1:
                if rond == 0 or rond == 1:
                    if signX > 0:
                        lines[i+y*signY:i+lastY*signY,j+signX*(x-1)] = True
                    else:
                        lines[i+lastY*signY:i+y*signY,j+signX*(x-1)] = True
                else:
                    if signX > 0:
                        lines[i+lastY*signY:i+y*signY,j+signX*(x-1)] = True
                        
                    else:
                        lines[i+y*signY:i+lastY*signY,j+signX*(x-1)] = True

            else:
                lines[i+y*signY,j+x*signX] = True
            x += 1
            lastY = y
        else:
            if rond == 0:
                rond += 1
                x = 0
                lastY = 0
                signY = -signY
                signX = -signX
            elif rond == 1:
                break
            elif rond == 2:
                signY = -signY
                signX = -signX
                x = 0
                lastY = 0
                rond += 1
            elif rond == 3:
                break

    return lines





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



for r in range(len(room)):
    for c in range(len(room[0])):
        if room[r,c] == 1:

            for ang in range(0,180,5):
                array = check_diag(r,c, ang)
                Y = list(np.where(array==True)[0])
                X = list(np.where(array==True)[1])
                Ynmr = Y.count(r)
                Xnmr = X.count(c)

                count = 0
                counter = 0

                if Ynmr <= Xnmr:
                    index = Y.index(r)
                else:
                    index = X.index(c)



                for i in range(index, len(Y)):
                    if room[Y[i],X[i]] == 1:
                        count += 1
                        counter = 0
                    else:
                        counter += 1
                        count += 1
                        if counter > 9:
                            count -= counter
                            counter = 0
                            break
                count -= counter
                counter = 0
                for i in range(index, 0, -1):
                    if room[Y[i],X[i]] == 1:
                        count += 1
                        counter = 0
                    else:
                        counter += 1
                        count += 1
                        if counter > 9:
                            count -= counter
                            counter = 0
                            break
                count -= counter

                print(ang, count)
            print(r,c)
            break
    if room[r,c] == 1:
        break



#print(room[np.where(array==True)])





#print(time.time()-start)
#room[np.where(array==True)] = 2
plt.imshow(room)

plt.show()