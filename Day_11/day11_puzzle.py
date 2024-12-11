def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.read().split()
    # fill the topographic map
    stones = [[],[]]
    for stone in datas:
        if stone in stones[0]:
            stone_index = stones[0].index(stone)
            stones[1][stone_index] += 1
        else:
            stones[0].append(stone)
            stones[1].append(1)
    # closing file
    my_file.close()
    # return the list
    return stones

def blink(stone):
    """
    Return, for a given stone, the list of stones
    created after a blink.
    """
    stones = []
    if (stone=='0'):
        stones = ['1']
    elif (len(stone)%2==0):
        # we take advantage of char here
        # to split the stone
        s = int(len(stone)/2)
        stones.append(str(int(stone[:s])))
        stones.append(str(int(stone[s:])))
    else:
        # multiply stone value and return it in a string format
        stones = [str(2024*int(stone))]
    return stones

def stonesBlink(stones):
    """
    The main idea is to work on a map data structure that give
    us, for a type of stone, its occurency.
    If we know that a stone s is present n times, we only have
    to perform once the blink operation, and update the blink
    result for stone s in new stone map. Each stone created by
    a blink on stone s will appear n times in the next stones map.
    """
    newStones = [[],[]]
    # for each type of stone
    for i in range(0,len(stones[0])):
        stone = stones[0][i]
        # we compute the stones created by blink
        locNewStones = blink(stone)
        # we update the occurency of the new stones,
        # in the newStones map
        for locNewStone in locNewStones:
            # if the stone type already exists, we increase
            # the occurency value accordingly
            if locNewStone in newStones[0]:
                i_newStone = newStones[0].index(locNewStone)
                newStones[1][i_newStone] += stones[1][i]
            # else, we create this stone type entry,
            # and init the occurency value
            else:
                newStones[0].append(locNewStone)
                newStones[1].append(stones[1][i])
    return newStones

def getStonesLength(stones):
    sum = 0
    for i in range(0,len(stones[0])):
        sum += stones[1][i]
    return sum

def solve(input_file, nbrBlinks):
    stones = read_datas(input_file)
    for i in range(0,nbrBlinks):
        stones = stonesBlink(stones)
    return getStonesLength(stones)

# unit tests
stones_test = read_datas("day11_data_test.txt")
assert(blink('0')==['1'])
assert(blink('1')==['2024'])
assert(blink('2000')==['20','0'])
assert(solve("day11_data_test.txt",25)==55312)
# print solutions
print("Number of stones after 25 blinks:",solve("day11_data.txt",25))
print("Number of stones after 75 blinks:",solve("day11_data.txt",75))