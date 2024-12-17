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
                l.append(char)
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

def push(map, pos, side):
    # first, we get the sequence of adjacent objects
    i = 0
    while (map[pos[0]+(i+1)*side[0]][pos[1]+(i+1)*side[1]] == 'O'):
        i += 1
    # if next cell in empty space, we push everything from one
    if (map[pos[0]+(i+1)*side[0]][pos[1]+(i+1)*side[1]] == '.'):
        map[pos[0]+(i+1)*side[0]][pos[1]+(i+1)*side[1]] = 'O'
        map[pos[0]+side[0]][pos[1]+side[1]] = '@'
        map[pos[0]][pos[1]] = '.'
        newPosition = (pos[0]+side[0],pos[1]+side[1])
    else:
        newPosition = pos
    return map, newPosition

def moveRobot(map, pos, side):
    # move robots on the cell if it is available
    if (map[pos[0]+side[0]][pos[1]+side[1]] == '.'):
        map[pos[0]][pos[1]] = '.'
        map[pos[0]+side[0]][pos[1]+side[1]] = '@'
        newPosition = (pos[0]+side[0], pos[1]+side[1])
    # if it is an object, we have to push it
    elif (map[pos[0]+side[0]][pos[1]+side[1]] == 'O'):
        map, newPosition = push(map, pos, side)
    # in case this is a wall, nothing happen
    else:
        newPosition = pos
    return map, newPosition

def getBoxesGPSCoords(map):
    sum = 0
    for i in range(0,len(map)):
        for j in range(0,len(map[i])):
            if map[i][j] == 'O':
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
assert(getRobotPosition(map_test)==(2,2))
assert(solve("day15_data_test.txt")==10092)

# print solution
print("Sum of all boxes' GPS coordinates:", solve("day15_data.txt"))