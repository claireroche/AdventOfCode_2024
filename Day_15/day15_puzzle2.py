def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.readlines()
    # fill the grid and movements
    map = []
    moves = []
    for line in datas:
        line = line.strip()
        if (len(line) > 0 and line[0] == '#'):
            l = []
            for char in line:
                if char=='#':
                    l += ['#','#']
                elif char=='O':
                    l += ['[',']']
                elif char=='@':
                    l += ['@','.']
                else:
                    l += ['.','.']
            map.append(l)
        else:
            for char in line:
                moves.append(char)
    # closing file
    my_file.close()
    # return the lists
    return map, moves

def getRobotPosition(map):
    i = 1
    while (i < len(map)-1):
        j = 1
        while (j < len(map[0])-1):
            if (map[i][j] == '@'):
                return (i, j)
            j += 1
        i += 1
    print("getRobotPosition: position not found.")
    return (0,0)

def pushH(map, pos, side):
    # first, we get the sequence of adjacent objects
    i = 1
    boxes = [pos]
    while map[pos[0]][pos[1]+i*side] == '[' or map[pos[0]][pos[1]+i*side] == ']':
        boxes.append((pos[0],pos[1]+i*side))
        i += 1
    # if next cell is empty space, we push everything from one
    if (map[pos[0]][pos[1]+i*side] == '.'):
        #print(boxes)
        for i in range(0,len(boxes)):
            boxe = boxes.pop()
            map[boxe[0]][boxe[1]+side] = map[boxe[0]][boxe[1]]
            map[boxe[0]][boxe[1]] = '.'
        newPosition = (pos[0],pos[1]+side)
    else:
        newPosition = pos
    return map, newPosition

def areVPushable(map, boxes, side):
    """
    Return 1 if pushable, -1 if unknown, 0 if not
    """
    pushable = 1 # Yes
    for cell in boxes:
        if map[cell[0]+side][cell[1]] == '#':
            return 0
        elif map[cell[0]+side][cell[1]] == '[' or map[cell[0]+side][cell[1]] == ']':
            pushable = -1
    return pushable

def getAdjBoxes(map, boxes, side):
    adjBoxes = []
    for cell in boxes:
        if map[cell[0]+side][cell[1]] == '[':
            # add adj '[' and ']' boxes
            if (cell[0]+side, cell[1]  ) not in adjBoxes:
                adjBoxes.append((cell[0]+side, cell[1]  ))
            if ((cell[0]+side, cell[1]+1)) not in adjBoxes:
                adjBoxes.append((cell[0]+side, cell[1]+1))
        elif map[cell[0]+side][cell[1]] == ']':
            if (cell[0]+side, cell[1]  ) not in adjBoxes:
                adjBoxes.append((cell[0]+side, cell[1]  ))
            if ((cell[0]+side, cell[1]-1)) not in adjBoxes:
                adjBoxes.append((cell[0]+side, cell[1]-1))
    return adjBoxes

def pushVBoxes(map, boxes, side):
    for cell in boxes:
        map[cell[0]+side][cell[1]] = map[cell[0]][cell[1]]
        map[cell[0]][cell[1]] = '.'
    return map

def pushV(map, pos, side):
    boxes = [pos]
    listBoxes = [boxes]
    isPushable = areVPushable(map, boxes, side)
    newPosition = pos
    while isPushable == -1:
        boxes = getAdjBoxes(map, boxes, side)
        isPushable = areVPushable(map, boxes, side)
        if len(boxes) > 0:
            listBoxes.append(boxes)
    if isPushable == 1:
        for i in range(0,len(listBoxes)):
            boxes = listBoxes.pop()
            map = pushVBoxes(map, boxes, side)
            newPosition = (pos[0]+side,pos[1])
    return map, newPosition

def moveRobot(map, pos, side):
    if map[pos[0]+side[0]][pos[1]+side[1]] == '.':
        map[pos[0]][pos[1]] = '.'
        map[pos[0]+side[0]][pos[1]+side[1]] = '@'
        newPosition = (pos[0]+side[0], pos[1]+side[1])
    # if it is an object, we have to push it
    elif map[pos[0]+side[0]][pos[1]+side[1]] == '[' or map[pos[0]+side[0]][pos[1]+side[1]] == ']':
        if side==(0,-1):
            map, newPosition = pushH(map, pos, -1)
        elif side==(0,1):
            map, newPosition = pushH(map, pos, 1)
        elif side==(-1,0):
            map, newPosition = pushV(map, pos, -1)
        elif side==(1,0):
            map, newPosition = pushV(map, pos, 1)
        else:
            print("moveRobot: unknown side.")
    # in case this is a wall, nothing happen
    else:
        newPosition = pos
    return map, newPosition

def getBoxesGPSCoords(map):
    sum = 0
    for i in range(0,len(map)):
        for j in range(0,len(map[i])):
            if map[i][j] == '[':
                sum += 100*i + j
    return sum

def solve(input_file):
    map, moves = read_datas(input_file)
    robotPos = getRobotPosition(map)
    for i in range(0,len(moves)):
        if moves[i] == '<':
            map, robotPos = moveRobot(map, robotPos, (0,-1))
        elif moves[i] == '>':
            map, robotPos = moveRobot(map, robotPos, (0,1))
        elif moves[i] == '^':
            map, robotPos = moveRobot(map, robotPos, (-1,0))
        elif moves[i] == 'v':
            map, robotPos = moveRobot(map, robotPos, (1,0))
        else:
            print("solve: unknown move.")
    return getBoxesGPSCoords(map)

# unit tests
map_test, moves_test = read_datas("day15_data_test1.txt")
robotPos_test = getRobotPosition(map_test)
assert(solve("day15_data_test.txt")==9021)

# print solution
print("Sum of all boxes' GPS coordinates:", solve("day15_data.txt"))