import sys

def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.readlines()
    # fill the maze
    maze = []
    for line in datas:
        line = line.strip()
        l = []
        for char in line:
            l += [char]
        maze.append(l)
    # closing file
    my_file.close()
    # return the maze
    return maze

def getStart(maze):
    start = (0,0)
    for i in range(1,len(maze)-1):
        for j in range(1,len(maze[i])-1):
            if maze[i][j] == 'S':
                return (i,j)
    return start

def getEnd(maze):
    start = (0,0)
    for i in range(1,len(maze)-1):
        for j in range(1,len(maze[i])-1):
            if maze[i][j] == 'E':
                return (i,j)
    return start

def initDistancesMap(maze, start):
    distMap = {}
    freeCells = []
    for i in range(1,len(maze)-1):
        for j in range(1,len(maze[i])-1):
            if maze[i][j] !='#':
                distMap[(i,j)] = sys.maxsize
                freeCells.append((i,j))
    distMap[start] = 0
    return distMap, freeCells

def getWeight(states, distMap, tmp_weight, pos1, pos2):
    weight = 1
    side = pos2[0]-pos1[0],pos2[1]-pos1[1]
    if pos1 in tmp_weight:
        weight = 1
    elif side != states[pos1]:
            weight = 1001
    elif (pos2[0]+side[0],pos2[1]+side[1]) not in distMap:
        tmp_weight.append(pos2)
        weight = 1001
    return weight, tmp_weight

def updateState(states, pos1, pos2):
    states[pos2] = (pos2[0]-pos1[0],pos2[1]-pos1[1])
    return states

def updateAdjDistances(distMap, states, tmp_weight, pos1, pos2, previousPos):
    if pos2 in distMap:
        weight, tmp_weight = getWeight(states, distMap, tmp_weight, pos1, pos2)
        if distMap[pos2] > distMap[pos1] + weight:
            distMap[pos2] = distMap[pos1] + weight
            # update states
            states = updateState(states, pos1, pos2)
            previousPos[pos2] = pos1
    return distMap, states

def getMinElement(freeCells, distMap, states):
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
    while cell != start:
        path += [cell]
        cell = previousPos[cell]
    path += [start]
    return path

def getPathCost(path, states, distMap):
    cost = len(path)-1
    for i in range(0,len(path)-1):
        if states[path[i]] != states[path[i+1]]:
            #print("turn", path[i], path[i+1])
            cost += 1000
    #print(path[-1])
    return cost

def printMaze(maze,path,states):
    for cell in path:
        if states[cell] == (1,0):
            maze[cell[0]][cell[1]] = "v"
        if states[cell] == (-1,0):
            maze[cell[0]][cell[1]] = "^"
        if states[cell] == (0,-1):
            maze[cell[0]][cell[1]] = "<"
        if states[cell] == (0,1):
            maze[cell[0]][cell[1]] = ">"
    for i in range(0,len(maze)):
        char = ''
        for j in range(0,len(maze[i])):
            char += maze[i][j]
        print(char)

def solve(input_file):
    # read input datas
    maze = read_datas(input_file)
    # get start and end positions
    start = getStart(maze)
    end = getEnd(maze)
    # init distance map, and non-visited cells heap
    distMap, freeCells = initDistancesMap(maze, start)
    # init state (directions) map
    states = {}
    for cell in distMap:
        states[cell] = (0,0)
    states[start] = (0,1)
    # init previous positions map
    previousPos = {}
    tmp_weight = []
    pos = start
    while len(freeCells) > 0 and pos!=end:
        #print("==================")
        # get min position
        pos = getMinElement(freeCells, distMap, states)
        #print("Current pos:", pos, "distance:", distMap[pos], "state", states[pos])
        # remove from heap
        freeCells.pop(freeCells.index(pos))
        # update distance map
        distMap, states = updateAdjDistances(distMap, states, tmp_weight, pos, (pos[0]+1, pos[1]  ), previousPos)
        distMap, states = updateAdjDistances(distMap, states, tmp_weight, pos, (pos[0]-1, pos[1]  ), previousPos)
        distMap, states = updateAdjDistances(distMap, states, tmp_weight, pos, (pos[0]  , pos[1]+1), previousPos)
        distMap, states = updateAdjDistances(distMap, states, tmp_weight, pos, (pos[0]  , pos[1]-1), previousPos)
        if pos in tmp_weight:
            tmp_weight.pop(tmp_weight.index(pos))
        #print("distances:", distMap)
    # build the path
    path = buildPath(previousPos, start, end)
    #printMaze(maze,path,states)
    #print(distMap)
    #print(getPathCost(path, states, distMap))
    return getPathCost(path, states, distMap)

# unit test
maze_test = read_datas("day16_data_test.txt")
#print(maze_test)
assert(getStart(maze_test) == (13,1))
assert(getEnd(maze_test) == (1,13))
assert(solve("day16_data_test.txt")==7036)
assert(solve("day16_data_test2.txt")==11048)
assert(solve("day16_data_test3.txt")==21148)
assert(solve("day16_data_test5.txt")==4013)

# solve puzzle
print("Lowest score Reindeer can possibly get:", solve("day16_data.txt"))