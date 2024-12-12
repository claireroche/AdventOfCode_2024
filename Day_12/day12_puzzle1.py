def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.readlines()
    # fill the garden
    garden = []
    for line in datas:
        line = line.strip()
        L = []
        for char in line:
            L.append(char)
        garden.append(L)
    # closing file
    my_file.close()
    # return the list
    return garden

def isOutGarden(garden, i, j):
    return (i < 0 or j < 0 or i >= len(garden) or j >= len(garden[i]))

def updateAreaHeap(garden, areaHeap, perimeter, flower, cell):
    # if the flower at cell has the same type, we put it in
    # the area heap as a flower to treat
    isAlreadyInHeap = (cell in areaHeap)
    isOut = isOutGarden(garden, cell[0], cell[1])
    if (not isOut and garden[cell[0]][cell[1]]==flower and not isAlreadyInHeap):
        areaHeap.append(cell)
    # else, we increase the perimeter by one, as we have to
    # separate with a fence
    else:
        perimeter += 1
    return areaHeap, perimeter

def getAreaPerimeter(garden, cellStart):
    perimeter = 0
    area = []
    areaHeap = [cellStart]
    flower = garden[cellStart[0]][cellStart[1]]
    # 
    while (len(areaHeap) != 0):
        cell = areaHeap.pop()
        area.append(cell)
        isTreated = ([cell[0]+1,cell[1]] in areaHeap or [cell[0]+1,cell[1]] in area)
        if (not isTreated):
            areaHeap, perimeter = updateAreaHeap(garden, areaHeap, perimeter, flower, [cell[0]+1,cell[1]])
        isTreated = ([cell[0]-1,cell[1]] in areaHeap or [cell[0]-1,cell[1]] in area)
        if (not isTreated):
            areaHeap, perimeter = updateAreaHeap(garden, areaHeap, perimeter, flower, [cell[0]-1,cell[1]])
        isTreated = ([cell[0],cell[1]+1] in areaHeap or [cell[0],cell[1]+1] in area)
        if (not isTreated):
            areaHeap, perimeter = updateAreaHeap(garden, areaHeap, perimeter, flower, [cell[0],cell[1]+1])
        isTreated = ([cell[0],cell[1]-1] in areaHeap or [cell[0],cell[1]-1] in area)
        if (not isTreated):
            areaHeap, perimeter = updateAreaHeap(garden, areaHeap, perimeter, flower, [cell[0],cell[1]-1])
    return area, perimeter

def getAreaPrice(garden, cellStart):
    area, perimeter = getAreaPerimeter(garden, cellStart)
    return len(area)*perimeter

def initIsTreated(garden):
    isTreated = []
    for i in range(0,len(garden)):
        l = []
        for j in range(0,len(garden[i])):
            l.append(False)
        isTreated.append(l)
    return isTreated

def solve(input_file):
    garden = read_datas(input_file)
    totalPrice = 0
    isTreated = initIsTreated(garden)
    # we go through all the cells in the garden
    for i in range(0,len(garden)):
        for j in range(0,len(garden[i])):
            # if the cell is not an already treated area
            # we compute the whole area cells, and its
            # perimeter
            if (not isTreated[i][j]):
                area, perimeter = getAreaPerimeter(garden, [i,j])
                totalPrice += len(area)*perimeter
                for cell in area:
                    # mark area cells as treated
                    isTreated[cell[0]][cell[1]] = True
    return totalPrice

# unit tests
garden_test = read_datas("day12_data_test.txt")
assert(isOutGarden(garden_test, 0, 0)==False)
assert(getAreaPrice(garden_test, [4, 7])==4)
assert(getAreaPrice(garden_test, [0, 0])==216)
assert(solve("day12_data_test.txt")==1930)
# print solution
print("Total fence price:",solve("day12_data.txt"))