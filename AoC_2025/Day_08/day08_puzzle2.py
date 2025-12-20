import sys
import math

def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # reading the file 
    data = my_file.readlines()
    # store diagram, and add ghost boundaries
    boxes = []
    for line in data:
        boxeChar = line.strip().split(',')
        boxe = [int(boxeChar[0]), int(boxeChar[1]), int(boxeChar[2])]
        boxes.append(boxe)
    # closing file
    my_file.close()
    # return the lists
    return boxes

def straightLineDistance(boxe1, boxe2):
    distance = pow(boxe2[0]-boxe1[0], 2)
    distance += pow(boxe2[1]-boxe1[1], 2)
    distance += pow(boxe2[2]-boxe1[2], 2)
    return math.sqrt(distance)

def computeDistanceMap(boxes):
    distanceMap = {}
    for i in range(len(boxes)-1):
        boxe1 = boxes[i]
        for j in range(i+1, len(boxes)):
            boxe2 = boxes[j]
            if boxe1 != boxe2:
                distance = straightLineDistance(boxe1, boxe2)
                # we consider here that each distance is uniq.
                # there is no good reason for this to be true.
                distanceMap[distance] = [boxe1, boxe2]
    # sort the distanceMap by keys (distances)
    distanceMap = dict(sorted(distanceMap.items()))
    return distanceMap

def initCircuits(boxes):
    circuits = []
    for boxe in boxes:
        circuits.append([boxe])
    return circuits

def findBoxeCircuit(boxe, circuits):
    indexCircuit = 0
    found = False
    while not found:
        if boxe in circuits[indexCircuit]:
            found = True
        else:
            indexCircuit += 1
    return indexCircuit

def connectBoxes(circuits, boxe1, boxe2):
    indexCircuit1 = findBoxeCircuit(boxe1, circuits)
    indexCircuit2 = findBoxeCircuit(boxe2, circuits)
    if indexCircuit1 != indexCircuit2:
        # we need to fuse two circuits
        circuit1 = circuits[indexCircuit1]
        circuit2 = circuits[indexCircuit2]
        circuits.remove(circuit1)
        circuits.remove(circuit2)
        circuits.append(circuit1 + circuit2)
    return circuits

def connectNClosestBoxes(boxes, distanceMap):
    # init circuits list
    circuits = initCircuits(boxes)
    for distance in distanceMap:
        boxe1 = distanceMap[distance][0]
        boxe2 = distanceMap[distance][1]
        circuits = connectBoxes(circuits, boxe1, boxe2)
        if len(circuits) == 1:
            return boxe1[0]*boxe2[0]
    return 0

def solve(input_file):
    boxes = read_datas(input_file)
    distanceMap = computeDistanceMap(boxes)
    return connectNClosestBoxes(boxes, distanceMap)

# unit tests
boxes_test = read_datas("day08_data_test.txt")
assert(len(boxes_test) == 20)
assert(len(boxes_test[0]) == 3)
assert(boxes_test[0] == [162,817,812])
distanceMap_test = computeDistanceMap(boxes_test)
assert(distanceMap_test[next(iter(distanceMap_test))] == [[162,817,812], [425,690,689]])
assert(solve("day08_data_test.txt") == 25272)

# print solution
if len(sys.argv) > 1:
    print("Result if you multiply together the X coordinates of the last two junction boxes you need to connect: ", solve(sys.argv[1]))