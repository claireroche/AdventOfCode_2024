def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.read()
    # fill each number in a list
    denseDiskMap = []
    ID_number = 0
    for i in range (0,int(len(datas)/2)):
        denseDiskMap.append([ID_number, int(datas[2*i])])
        denseDiskMap.append([-1, int(datas[2*i+1])])
        ID_number += 1
    denseDiskMap.append([ID_number, int(datas[-1])])
    # append fake space at end of line
    denseDiskMap.append([-1, 0])
    # closing file
    my_file.close()
    # return the list
    return denseDiskMap

def swapFiles(denseDiskMap, i, j):
    """
    Here, i is the index of the blank space, and j the index of
    the files to move.
    We assume here that j > i.
    """
    newDenseDiskMap = []
    for file in denseDiskMap:
        newDenseDiskMap.append(file.copy())
    if (j-i > 1):
        # we update the blank spaces
        # position j becomes a space (so -1)
        newDenseDiskMap[j][0] = -1
        # we glue the space before and after to it
        newDenseDiskMap[j][1] += denseDiskMap[j-1][1] + denseDiskMap[j+1][1]
        newDenseDiskMap.pop(j+1)
        newDenseDiskMap.pop(j-1)
        # update the new blank space, and the new value position
        # the previous space is now size 0
        newDenseDiskMap[i][1] = 0
        # we insert the files after this 0 size space
        newDenseDiskMap.insert(i+1, denseDiskMap[j])
        # we insert the new space after the swap files
        newDenseDiskMap.insert(i+2, [-1, denseDiskMap[i][1]-denseDiskMap[j][1]])
    elif (j-i == 1):
        # annoying edge case...
        newDenseDiskMap[i], newDenseDiskMap[j] = denseDiskMap[j], denseDiskMap[i]
        newDenseDiskMap[j+1][1] += denseDiskMap[j][1]
        newDenseDiskMap.pop(j)
        # we insert the new space of length 0 in front of file
        newDenseDiskMap.insert(i,[-1,0])
    return newDenseDiskMap

def reArrangeFiles(denseDiskMap):
    """
    This method aims to swap whole files from right to left 
    in "most left" available spaces.
    We note that all even index positions are files, while
    each odd index position correspond to the space between
    two files.
    """
    newDenseDiskMap = []
    for file in denseDiskMap:
        newDenseDiskMap.append(file.copy())
    # we start by the last file
    ind_file = len(denseDiskMap)-2
    while (ind_file >= 2):
        isMoved = False
        ind_space = 1
        # we loop over the spaces before ind_file,
        # to find one with available space to swap with file.
        while((not isMoved) and ind_space < ind_file):
            if (newDenseDiskMap[ind_space][1] >= newDenseDiskMap[ind_file][1]):
                newDenseDiskMap = swapFiles(newDenseDiskMap, ind_space, ind_file)
                isMoved = True
            # next space to check is next odd position (in +2)
            ind_space += 2
        if (not isMoved):
            # if the checked file didn't move, we have to decrease the index
            # if it didn't move, we don't need to change the index.
            ind_file -= 2
    return newDenseDiskMap

def buildSparseDiskMap(denseDiskMap):
    """
    Build the sparse disk map, from the dense disk map.
    Here, we assume that the dense disk map is made of an odd number of elements.
    """
    sparseDiskMap = []
    # let us notice that i corresponds here to the ID number
    for i in range(0, int(len(denseDiskMap)/2)):
        # add block of numbers of ID number = denseDiskMap[2*i][0]
        sparseDiskMap += [denseDiskMap[2*i][0]]*denseDiskMap[2*i][1]
        # add following block of void
        sparseDiskMap += ['.']*denseDiskMap[2*i+1][1]
    return sparseDiskMap

def computeChecksum(sparseDiskMap):
    sum = 0
    for i in range(1,len(sparseDiskMap)):
        if (sparseDiskMap[i] != '.'):
            sum += i*sparseDiskMap[i]
    return sum

def solve(input_file):
    denseDiskMap = read_datas(input_file)
    # swap files from right to left in "most left" available spaces
    reArrangedDiskMap = reArrangeFiles(denseDiskMap)
    # build the sparse disk map
    sparseDiskMap = buildSparseDiskMap(reArrangedDiskMap)
    return computeChecksum(sparseDiskMap)

# unit tests
denseDiskMap_test = read_datas("day09_data_test.txt")
assert(len(denseDiskMap_test)==20)  # 19 + fake space
assert(denseDiskMap_test[18]==[9,2])
reArrangedDiskMap_test = reArrangeFiles(denseDiskMap_test)
sparseDiskMap_test = buildSparseDiskMap(reArrangedDiskMap_test)
assert(solve("day09_data_test.txt")==2858)
# print solution
print("Resulting filesystem checksum: ",solve("day09_data.txt"))