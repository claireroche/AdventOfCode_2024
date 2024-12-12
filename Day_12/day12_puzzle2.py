def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.readlines()
    # fill the garden
    garden = []
    ghost_line = []
    for i in range(0,len(datas[0])+2):
        ghost_line.append('.')
    garden.append(ghost_line.copy())
    for line in datas:
        line = line.strip()
        L = ['.']
        for char in line:
            L.append(char)
        L.append('.')
        garden.append(L)
    garden.append(ghost_line.copy())
    # closing file
    my_file.close()
    # return the list
    return garden

def isOutGarden(garden, i, j):
    return (i < 0 or j < 0 or i >= len(garden) or j >= len(garden[i]))

def isCorner(garden, i, j):
    """
    For a given cell in the garden, we compute if it is
    a corner in its area. If so, we also compute the
    number of corners of this cell in its area.
    Let us note that on one celle, we can have many corners.
    A corner can happen in two configurations:
       xxx         xxx
    1. x00      2. x00
       x00         x0x
    With 4 positions possible (all around the cell).
    In this method, we check the 8 configurations possibles
    for the cell.
    Example of cell 0 which has 4 corners:
    xxx
    x0x
    xxx
    """
    isC = False
    nbrEdges = 0
    flower = garden[i][j]
    if (garden[i][j-1] != flower and garden[i-1][j] != flower):
        isC = True
        nbrEdges += 1
    if (garden[i-1][j] != flower and garden[i][j+1] != flower):
        isC = True
        nbrEdges += 1
    if (garden[i][j+1] != flower and garden[i+1][j] != flower):
        isC = True
        nbrEdges += 1
    if (garden[i+1][j] != flower and garden[i][j-1] != flower):
        isC = True
        nbrEdges += 1 
    
    # test second case of corners
    if (garden[i][j-1] == flower and garden[i-1][j] == flower and garden[i-1][j-1] != flower):
        isC = True
        nbrEdges += 1
    if (garden[i-1][j] == flower and garden[i][j+1] == flower and garden[i-1][j+1] != flower):
        isC = True
        nbrEdges += 1
    if (garden[i][j+1] == flower and garden[i+1][j] == flower and garden[i+1][j+1] != flower):
        isC = True
        nbrEdges += 1
    if (garden[i+1][j] == flower and garden[i][j-1] == flower and garden[i+1][j-1] != flower):
        isC = True
        nbrEdges += 1 

    return isC, nbrEdges

def updateAreaHeap(garden, areaHeap, flower, cell):
    # if the flower at cell has the same type, we put it in
    # the area heap as a flower to treat
    isAlreadyInHeap = (cell in areaHeap)
    isOut = isOutGarden(garden, cell[0], cell[1])
    if (not isOut and garden[cell[0]][cell[1]]==flower and not isAlreadyInHeap):
        areaHeap.append(cell)
    return areaHeap

def getArea(garden, cellStart):
    area = []
    areaHeap = [cellStart]
    flower = garden[cellStart[0]][cellStart[1]]
    # 
    while (len(areaHeap) != 0):
        cell = areaHeap.pop()
        area.append(cell)
        isTreated = ([cell[0]+1,cell[1]] in areaHeap or [cell[0]+1,cell[1]] in area)
        if (not isTreated):
            areaHeap = updateAreaHeap(garden, areaHeap, flower, [cell[0]+1,cell[1]])
        isTreated = ([cell[0]-1,cell[1]] in areaHeap or [cell[0]-1,cell[1]] in area)
        if (not isTreated):
            areaHeap = updateAreaHeap(garden, areaHeap, flower, [cell[0]-1,cell[1]])
        isTreated = ([cell[0],cell[1]+1] in areaHeap or [cell[0],cell[1]+1] in area)
        if (not isTreated):
            areaHeap = updateAreaHeap(garden, areaHeap, flower, [cell[0],cell[1]+1])
        isTreated = ([cell[0],cell[1]-1] in areaHeap or [cell[0],cell[1]-1] in area)
        if (not isTreated):
            areaHeap = updateAreaHeap(garden, areaHeap, flower, [cell[0],cell[1]-1])
    return area

def initIsTreated(garden):
    isTreated = []
    for i in range(0,len(garden)):
        l = []
        for j in range(0,len(garden[i])):
            if (garden[i][j] != '.'):
                l.append(False)
            else:
                l.append(True)
        isTreated.append(l)
    return isTreated

def getAreaPrice(garden, area):
    nbrEdges = 0
    for cell in area:
        # count corners in area
        isC, nbrCorners = isCorner(garden, cell[0], cell[1])
        if isC:
            nbrEdges += nbrCorners
    return len(area)*nbrEdges

def solve(input_file):
    garden = read_datas(input_file)
    totalPrice = 0
    isTreated = initIsTreated(garden)
    # we go through all the cells in the garden
    for i in range(1,len(garden)-1):
        for j in range(1,len(garden[i])-1):
            # if the cell is not an already treated area
            # we compute the whole area cells, and its
            # price
            if (not isTreated[i][j]):
                area = getArea(garden, [i,j])
                for cell in area:
                    # mark area cells as treated
                    isTreated[cell[0]][cell[1]] = True
                totalPrice += getAreaPrice(garden, area)
    return totalPrice

# unit tests
garden_test = read_datas("day12_data_test.txt")
assert(isOutGarden(garden_test, 0, 0)==False)
assert(isCorner(garden_test, 1, 1)==(True,1))
assert(isCorner(garden_test, 3, 3)==(True,1))
assert(solve("day12_data_test.txt")==1206)
# print solution
print("Total fence price:",solve("day12_data.txt"))