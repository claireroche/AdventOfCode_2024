def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # reading the file 
    data = my_file.readlines()
    # separate the two columns
    map = []
    for line in data:
        line = line.strip()
        line_list = []
        for char in line:
            line_list.append(char)
        map.append(line_list)
    # closing file
    my_file.close()
    # return the lists
    return map

def isOut(map, i, j):
    """
    Return True if position (i,j) is in the map, False otherwise.
    """
    return (i>=len(map) or i<0 or j >= len(map[i]) or j<0)
    
def isObstruction(map, i, j):
    """
    Return True if the cell (i,j) of the map is obstructed (with an object '#' or 'O' for temporary obstacles), False otherwise.
    """
    return (not isOut(map, i, j) and (map[i][j] == '#' or map[i][j] == 'O'))

def getGuardPosition(map):
    """
    Find the guard position in the map. This position is supposed to be uniq.
    Here, we define the position using 3 things:
    position[0] : is the i coordinate of the guard on the map
    position[1] : is the j coordinate of the guard on the map
    position[2] : is the side of the guard (ex: ">", he's walking in the right direction)
    """
    for i in range(0,len(map)):
        for j in range(0,len(map[i])):
            if (map[i][j] == '^' or map[i][j] == '>' or map[i][j] == 'v' or map[i][j] == '<'):
                return [i, j, map[i][j]]
    print("getGuardPosition: guard not found.")

def turnRight(position):
    """
    Turn  right the position of the guard (third information of the position list) with 90 degrees.
    """
    if (position[2] == '^'):
        return [position[0], position[1], '>']
    elif (position[2] == '>'):
        return [position[0], position[1], 'v']
    elif (position[2] == 'v'):
        return [position[0], position[1], '<']
    elif (position[2] == '<'):
        return [position[0], position[1], '^']
    else:
        print("turnRight: unknown starting side.")

def takeStep(position):
    """
    The guard takes on step in is current direction.
    """
    if (position[2] == '^'):
        return [position[0]-1, position[1], position[2]]
    elif (position[2] == '>'):
        return [position[0], position[1]+1, position[2]]
    elif (position[2] == 'v'):
        return [position[0]+1,position[1], position[2]]
    elif (position[2] == '<'):
        return [position[0], position[1]-1, position[2]]
    else:
        print("takeStep: unknown starting side.")

def move(map, position):
    """
    Get the next move of the guard, and update the map with the visited cells.
    """
    # compute the guard position in case he takes one step forward
    step_position = takeStep(position)
    # if the cell is not obstructed, we move the guard
    if (not isObstruction(map, step_position[0], step_position[1])):
        # reset the cell the guard is leaving to init value
        position = takeStep(position)
    # if the cell is obstructed, the guard turns right but does not change cell
    else:
        position = turnRight(position)
    return position

def getPath(map, start_position):
    # list of visited positions
    visited_positions = []
    # get init position
    position = start_position
    # compute guard path
    # here, not(position in visited_positions) helps us to detect if the guard is in a loop.
    # we assume that, if the guard came back at the same position, with the same direction
    # than previously, than, he will repeat the same path, so we can stop.
    while (not(position in visited_positions) and not isOut(map, position[0], position[1])):
        visited_positions.append(position)
        position = move(map, position)
    isLoop = (position in visited_positions)
    # return the list of visited position
    return visited_positions, isLoop

def solve(input_file):
    # read input datas
    map = read_datas(input_file)
    # get init position
    init_position = getGuardPosition(map)
    # compute guard path
    # here, not(position in visited_positions) helps us to detect if the guard is in a loop.
    # we assume that, if the guard came back at the same position, with the same direction
    # than previously, than, he will repeat the same path, so we can stop.
    init_path, isInitLoop = getPath(map, init_position)
    # get the cells visited (avoid to get twice the same cells)
    cells = []
    # loop counter
    nbrLoops = 0
    for i in range(1,len(init_path)):
        # the idea here is to start to check the path by beginning right
        # at the place we put the obstacle, in order to avoid
        # useless previous un-changed part of path.
        starting_pos = init_path[i-1]
        obstacle_cell = [init_path[i][0], init_path[i][1]]
        if ( not obstacle_cell in cells):
            cells.append(obstacle_cell)
            # add a temporary obstacle on map
            map[obstacle_cell[0]][obstacle_cell[1]] = 'O'
            # get the visited positions, and also tells us if it is a loop
            path, isLoop = getPath(map, starting_pos)
            # remove the temporary obstacle on map
            map[obstacle_cell[0]][obstacle_cell[1]] = '.'
            # update count if it is a loop
            if (isLoop):
                nbrLoops += 1
    # return loops number
    return nbrLoops

# unit tests
map = read_datas("day06_data_test.txt")
assert(isOut(map,0,1)==False)
assert(isOut(map,-1,1)==True)
assert(isOut(map,101,3)==True)
assert(isObstruction(map,3,3)==False)
assert(isObstruction(map,3,2)==True)
assert(turnRight([1,2,'>'])[2] == 'v')
assert(turnRight([4,3,'v'])[2] == '<')
assert(turnRight([0,0,'<'])[2] == '^')
assert(turnRight([6,1,'^'])[2] == '>')
assert(takeStep([1,2,'>']) == [1,3,'>'])
assert(takeStep([1,2,'v']) == [2,2,'v'])
assert(takeStep([1,2,'<']) == [1,1,'<'])
assert(takeStep([1,2,'^']) == [0,2,'^'])
assert(getGuardPosition(map)[0]==6)
assert(getGuardPosition(map)[1]==4)
#print(solve("day06_data_test.txt"))
assert(solve("day06_data_test.txt")==6)
# print solution
print("Number of possible loops: ", solve("day06_data.txt"))