def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.read()
    # fill each number in a list
    denseDiskMap = []
    for char in datas:
        denseDiskMap.append(int(char))
    # closing file
    my_file.close()
    # return the list
    return denseDiskMap

def buildSparseDiskMap(denseDiskMap):
    """
    Build the sparse disk map, from the dense disk map.
    Here, we assume that the dense disk map is made of an odd number of elements.
    """
    sparseDiskMap = []
    # let us notice that i corresponds here to the ID number
    for i in range(0, int(len(denseDiskMap)/2)):
        # add block of numbers of ID number = i
        sparseDiskMap +=   [i]*denseDiskMap[2*i]
        # add following block of void
        sparseDiskMap += ['.']*denseDiskMap[2*i+1]
    # add last element
    sparseDiskMap += [int(len(denseDiskMap)/2)]*denseDiskMap[-1]
    return sparseDiskMap

def findFirstSpace(sparceDiskMap):
    for i in range(0,len(sparceDiskMap)):
        if (sparceDiskMap[i] == '.'):
            return i
    return 0

def swapAndEraseFreeSpace(sparseDiskMap):
    newDiskMap = sparseDiskMap.copy()
    # if last element is a blank space, we remove it
    if (newDiskMap[-1] == '.'):
        newDiskMap.pop()
    # else, we swap this element to the first found blank position
    else:
        index_firstSpace = findFirstSpace(sparseDiskMap)
        # replace first blank space by last element
        newDiskMap[index_firstSpace] = newDiskMap[-1]
        # remove last element, which should be a space now
        newDiskMap.pop()
    return newDiskMap

def moveBlocks(sparseDiskMap):
    """
    Move file blocks one at a time, until there is no
    blank space left.
    """
    newDiskMap = sparseDiskMap.copy()
    while ('.' in newDiskMap):
        newDiskMap = swapAndEraseFreeSpace(newDiskMap)
    return newDiskMap

def computeChecksum(compactedDiskMap):
    sum = 0
    for i in range(1,len(compactedDiskMap)):
        sum += i*compactedDiskMap[i]
    return sum

def solve(input_file):
    denseDiskMap = read_datas(input_file)
    sparseDiskMap = buildSparseDiskMap(denseDiskMap)
    compactDiskMap = moveBlocks(sparseDiskMap)
    return computeChecksum(compactDiskMap)

# unit tests
denseDiskMap_test = read_datas("day09_data_test.txt")
assert(len(denseDiskMap_test)==19)
assert(denseDiskMap_test[18]==2)
sparseDiskMap_test = buildSparseDiskMap(denseDiskMap_test)
assert(sparseDiskMap_test.count(3)==3)
assert(sparseDiskMap_test.count(8)==4)
assert(sparseDiskMap_test.count(9)==2)
compactDiskMap_test = moveBlocks(sparseDiskMap_test)
assert(len(compactDiskMap_test)==28)
assert(compactDiskMap_test[-1]==6)
assert(compactDiskMap_test[2]==9)
assert(solve("day09_data_test.txt")==1928)
# print result
print("Resulting filesystem checksum:", solve("day09_data.txt"))