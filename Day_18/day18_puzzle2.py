import sys

def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.readlines()
    # fill the list of falling bytes positions
    bytesPos = []
    for line in datas:
        line = line.strip().split(',')
        bytesPos.append((int(line[1]),int(line[0])))
    # closing file
    my_file.close()
    # return the bytes positions
    return bytesPos

def buildGrid(bytesPos, gridSize):
    grid = []
    for i in range(0,gridSize):
        row = []
        for j in range(0,gridSize):
            if (i,j) in bytesPos:
                row.append('#')
            else:
                row.append('.')
        grid.append(row)
    return grid

def initDistancesMap(grid,start):
    distMap = {}
    freeCells = []
    for i in range(0,len(grid)):
        for j in range(0,len(grid[i])):
            if grid[i][j] !='#':
                distMap[(i,j)] = sys.maxsize
                freeCells.append((i,j))
    distMap[start] = 0
    return distMap, freeCells

def updateAdjDistances(distMap, pos1, pos2, previousPos):
    if pos2 in distMap and distMap[pos2] > distMap[pos1] + 1:
            distMap[pos2] = distMap[pos1] + 1
            # update states
            previousPos[pos2] = pos1
    return distMap

def getMinElement(freeCells, distMap):
    cell = freeCells[0]
    minDist = distMap[cell]
    for i in range(1,len(freeCells)):
        if minDist > distMap[freeCells[i]]:
            cell = freeCells[i]
            minDist = distMap[cell]
    return cell

def buildPath(previousPos, start, end):
    cell = end
    path = []
    while cell != start and cell not in path:
        path += [cell]
        cell = previousPos[cell]
    path += [start]
    return path

def computePath(grid):
    # get start and end positions
    start = (0,0)
    end = (len(grid)-1, len(grid[-1])-1)
    # init distance map, and non-visited cells heap
    distMap, freeCells = initDistancesMap(grid, start)
    # init previous positions map
    previousPos = {}
    while len(freeCells) > 0:
        # get min position
        pos = getMinElement(freeCells, distMap)
        # remove from heap
        freeCells.pop(freeCells.index(pos))
        # update distance map
        distMap = updateAdjDistances(distMap, pos, (pos[0]+1, pos[1]  ), previousPos)
        distMap = updateAdjDistances(distMap, pos, (pos[0]-1, pos[1]  ), previousPos)
        distMap = updateAdjDistances(distMap, pos, (pos[0]  , pos[1]+1), previousPos)
        distMap = updateAdjDistances(distMap, pos, (pos[0]  , pos[1]-1), previousPos)
    # build the path
    if end in previousPos:
        path = buildPath(previousPos, start, end)
    # return an empty path list if end is not reached
    else:
        path = []
    return path

def printMaze(grid, path):
    for i in range(0,len(grid)):
        char = ''
        for j in range(0,len(grid[i])):
            if (i,j) in path:
                char += '0'
            else:
                char += grid[i][j]
        print(char)

def solve(input_file, sizeGrid, nbrFallenBytes):
    # read input datas
    bytesPos = read_datas(input_file)
    grid = buildGrid(bytesPos[0:nbrFallenBytes], sizeGrid)
    # compute init path
    path = computePath(grid)
    isValid = (len(path) >0)
    index_byte = nbrFallenBytes
    while index_byte < len(bytesPos) and isValid:
        if bytesPos[index_byte] in path:
            # update the grid first
            grid = buildGrid(bytesPos[0:index_byte+1], sizeGrid)
            # compute new path
            path = computePath(grid)
            # check if the path is valid
            isValid = (len(path) >0)
        index_byte += 1
    #printMaze(grid, path)
    # don't forget to invert again the positions (x,y),
    # as I did to read the input file.
    return bytesPos[index_byte-1][1],bytesPos[index_byte-1][0]

# unit test
bytesPos_test = read_datas("day18_data_test.txt")
assert(solve("day18_data_test.txt",7,12)==(6,1))

# solve puzzle
print("Minimum number of steps to take:", solve("day18_data.txt", 71, 1024))