def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.read().splitlines()
    # fill the topographic map
    topographicMap = []
    for line in datas:
        L = []
        for char in line:
            L.append(int(char))
        topographicMap.append(L)
    # closing file
    my_file.close()
    # return the list
    return topographicMap

def isOutMap(topographicMap, cell):
    return (cell[0] < 0 or cell[1] < 0 or cell[0] >= len(topographicMap) or cell[1] >= len(topographicMap[cell[0]]))

def updateTrailHeap(topographicMap, cell, cellNext, trailHeap):
    newTrailHeap = trailHeap.copy()
    if (not isOutMap(topographicMap, cellNext)):
        step = topographicMap[cellNext[0]][cellNext[1]] - topographicMap[cell[0]][cell[1]]
        if (step == 1):
            newTrailHeap.append(cellNext)
    return newTrailHeap

def getTrailScore(topographicMap, cellStart):
    """
    """
    trailHeap = [cellStart]
    score = 0
    while (not (len(trailHeap) == 0)):
        cell = trailHeap.pop()
        if (topographicMap[cell[0]][cell[1]]==9):
            score += 1
        else:
            trailHeap = updateTrailHeap(topographicMap, cell, (cell[0]-1, cell[1]  ), trailHeap)
            trailHeap = updateTrailHeap(topographicMap, cell, (cell[0]+1, cell[1]  ), trailHeap)
            trailHeap = updateTrailHeap(topographicMap, cell, (cell[0]  , cell[1]-1), trailHeap)
            trailHeap = updateTrailHeap(topographicMap, cell, (cell[0]  , cell[1]+1), trailHeap)
    return score

def solve(input_file):
    topographicMap = read_datas(input_file)
    score = 0
    for i in range(0, len(topographicMap)):
        for j in range(0, len(topographicMap)):
            if (topographicMap[i][j] == 0):
                score += getTrailScore(topographicMap, (i,j))
    return score

# unit tests
topographicMap_test1 = read_datas("day10_data_test1.txt")
#print(topographicMap_test1)
assert(isOutMap(topographicMap_test1, (-1,2))==True)
assert(isOutMap(topographicMap_test1, (2,5))==True)
assert(isOutMap(topographicMap_test1, (3,2))==False)

topographicMap_test2 = read_datas("day10_data_test2.txt")
#print(topographicMap_test2)
assert(getTrailScore(topographicMap_test2, (5,5))==4)
assert(getTrailScore(topographicMap_test2, (5,2))==1)
assert(getTrailScore(topographicMap_test2, (0,2))==20)
assert(getTrailScore(topographicMap_test2, (0,4))==24)
assert(solve("day10_data_test2.txt")==81)

# print solution
print("Sum of scores of all trailheads on the topographic map: ", solve("day10_data.txt"))