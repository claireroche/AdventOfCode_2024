import sys

def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # reading the file 
    data = my_file.readlines()
    # store diagram, and add ghost boundaries
    redTiles = []
    for line in data:
        tileChar = line.strip().split(',')
        redTile = [int(tileChar[0]), int(tileChar[1])]
        redTiles.append(redTile)
    # closing file
    my_file.close()
    # return the lists
    return redTiles

def getArea(tile1, tile2):
    dx = max(tile1[0], tile2[0])-min(tile1[0], tile2[0])+1
    dy = max(tile1[1], tile2[1])-min(tile1[1], tile2[1])+1
    area = dx*dy
    return area

def solve(input_file):
    redTiles = read_datas(input_file)
    largestArea = 0
    for i in range(0,len(redTiles)):
        for j in range(i+1, len(redTiles)):
            area = getArea(redTiles[i], redTiles[j])
            if (area > largestArea):
                largestArea = area
    return largestArea

# unit tests
redTiles_test = read_datas("day09_data_test.txt")
assert(getArea([7,3],[2,3]) == 6)
assert(getArea([7,1],[11,7]) == 35)
assert(getArea([2,5],[9,7]) == 24)
assert(solve("day09_data_test.txt") == 50)

# print solution
if len(sys.argv) > 1:
    print("Largest area of any rectangle: ", solve(sys.argv[1]))