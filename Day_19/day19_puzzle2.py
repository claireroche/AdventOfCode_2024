def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.readlines()
    # fill the list of available towels
    towels = []
    line = datas[0].strip().split(', ')
    for towel in line:
        towels.append(towel)
    # fill the wanted designs list
    designs = []
    index = 2
    while index < len(datas):
        line = datas[index].strip()
        designs.append(line)
        index += 1
    # closing file
    my_file.close()
    # return the towels available, and the wanted designs
    return towels, designs

def splitDesign(towels, design):
    """
    Brute force approach, for a given
    design, to build all the combinations
    possible using the available towels.
    """
    validDesigns = []
    heapDesigns = [[design]]
    while len(heapDesigns) > 0:
        # we take one design from the heap
        tmp_design = heapDesigns.pop()
        for i in range(1,len(tmp_design[-1])):
            # we split the design accordingly to towels set
            # and add those to the heap to treat
            if tmp_design[-1][0:i] in towels:
                heapDesigns.append(tmp_design[:-1]+[tmp_design[-1][:i], tmp_design[-1][i:]])
        # if the design is valid, we add it to the valid list
        if isValidDesign(towels, tmp_design):
            validDesigns.append(tmp_design)
    return validDesigns

def isValidDesign(towels, splittedDesign):
    """
    A design is here a list of sub-parts.
    A design is refered as valid if each
    sub-part is in the available towels list.
    """
    isValid = True
    for i in range(0,len(splittedDesign)):
        if splittedDesign[i] not in towels:
            return False
    return isValid

def isSplittable(towels, design, mapCombNumbers, invalidDesigns):
    if design in mapCombNumbers:
        return True, mapCombNumbers[design]
    elif design not in mapCombNumbers and len(design) < 2:
        return False, 0
    elif design in invalidDesigns:
        return False, 0
    else:
        count = 0
        for i in range(1,len(design)):
            if design[:i] in towels:
                isSplitRight, nbrRight = isSplittable(towels, design[i:], mapCombNumbers, invalidDesigns)
                count += nbrRight
                if isSplitRight and design[i:] not in mapCombNumbers:
                    mapCombNumbers[design[i:]] = nbrRight
                elif not isSplitRight and design[i:] not in invalidDesigns:
                    invalidDesigns.append(design[i:])
                i += 1
        return (count != 0), count
    
def initMapValidDesigns(towels):
    """
    The idea here is to build a map which gives,
    for each towel of towels, the number of way
    you can express it using other towels. We
    can use the "brute force" approach to init
    this map as it is made of a "short" set of
    "short" patterns.
    """
    mapValidDesigns = {}
    for towel in towels:
        mapValidDesigns[towel] = len(splitDesign(towels, towel))
    return mapValidDesigns

def solve(input_file):
    towels, designs = read_datas(input_file)
    mapValidDesigns = initMapValidDesigns(towels)
    invalidDesigns = []
    count = 0
    for design in designs:
        count += isSplittable(towels, design, mapValidDesigns, invalidDesigns)[1]
    return count

# unit tests
towels_test, designs_test = read_datas("day19_data_test.txt")
validDesigns = []
invalidDesigns = []
mapCombNumbers_test = initMapValidDesigns(towels_test)
assert(isSplittable(towels_test, designs_test[0], mapCombNumbers_test, invalidDesigns)[1]==2)
assert(isSplittable(towels_test, designs_test[1], mapCombNumbers_test, invalidDesigns)[1]==1)
assert(isSplittable(towels_test, designs_test[2], mapCombNumbers_test, invalidDesigns)[1]==4)
assert(isSplittable(towels_test, designs_test[3], mapCombNumbers_test, invalidDesigns)[1]==6)
assert(isSplittable(towels_test, designs_test[4], mapCombNumbers_test, invalidDesigns)[1]==0)
assert(isSplittable(towels_test, designs_test[5], mapCombNumbers_test, invalidDesigns)[1]==1)
assert(isSplittable(towels_test, designs_test[6], mapCombNumbers_test, invalidDesigns)[1]==2)
assert(isSplittable(towels_test, designs_test[7], mapCombNumbers_test, invalidDesigns)[1]==0)
assert(solve("day19_data_test.txt")==16)

# print solution
print("Number of possible designs:",solve("day19_data.txt"))