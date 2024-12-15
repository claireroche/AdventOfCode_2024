import re
import time
import numpy as np

def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.readlines()
    # fill the positions and velocities
    positions = []
    velocities = []
    index = 0
    for line in datas:
        line = line.strip()
        values = re.findall(r'-?\d+', line)
        positions.append([int(values[0]),int(values[1])])
        velocities.append([int(values[2]),int(values[3])])
    # closing file
    my_file.close()
    # return the list
    return positions, velocities

def moveRobot(position, velocitie, seconds):
    newPosition = []
    newPosition.append((position[0] + seconds*velocitie[0])%101) #%11)
    newPosition.append((position[1] + seconds*velocitie[1])%103) #%7)
    return newPosition

def countRobots(positions, velocities):
    """
        0   |   1   
    ------------------
        2   |   3
    """
    count = [0,0,0,0]
    tilesX = 101    #11
    tilesY = 103    #7
    for i in range(0,len(positions)):
        posRobot = moveRobot(positions[i],velocities[i],100)
        if (posRobot[0] <= tilesX//2-1 and posRobot[1] <= tilesY//2-1):
            count[0] += 1
        elif (posRobot[0] >= tilesX//2+1 and posRobot[1] <= tilesY//2-1):
            count[1] += 1
        elif (posRobot[0] <= tilesX//2-1 and posRobot[1] >= tilesY//2+1):
            count[2] += 1
        elif (posRobot[0] >= tilesX//2+1 and posRobot[1] >= tilesY//2+1):
            count[3] += 1
    return count[0]*count[1]*count[2]*count[3]

def buildGrid(positions):
    grid = []
    areAlignedStars = False
    for i in range(0,101):
        line = ""
        for j in range(0,103):
            if [i,j] in positions:
                line += "*"
            else:
                line += "."
        if '****' in line:
            areAlignedStars = True
        grid.append(line)
    if (areAlignedStars):
        # print grid
        for j in range(0,len(grid)):
            print(grid[j])
        time.sleep(2)
    return grid

def solve(input_file):
    positions, velocities = read_datas(input_file)
    for i in range(0,len(positions)):
        positions[i] = moveRobot(positions[i], velocities[i], 7093)
    grid = buildGrid(positions)
    for i in range(0,len(grid)):
        print(grid[i])
    return countRobots(positions, velocities)

# unit test
positions_test, velocities_test = read_datas("day14_data_test.txt")

# print solution
print("Safety factor after 100 seconds :",solve("day14_data.txt"))