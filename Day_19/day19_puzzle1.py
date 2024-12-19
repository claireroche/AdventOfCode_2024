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
    validDesigns = []
    heapDesigns = [[design]]
    while len(heapDesigns) > 0:
        tmp_design = heapDesigns.pop()
        for i in range(1,len(tmp_design[-1])):
            if tmp_design[-1] not in towels and tmp_design[-1][0:i] in towels:
                heapDesigns.append(tmp_design[:-1]+[tmp_design[-1][:i], tmp_design[-1][i:]])
                #print("add in heap", tmp_design[:-1]+[tmp_design[-1][:i], tmp_design[-1][i:]])
        if isValidDesign(towels, tmp_design):
            return True
    return False

def isValidDesign(towels, splittedDesign):
    isValid = True
    for i in range(0,len(splittedDesign)):
        if splittedDesign[i] not in towels:
            return False
    return isValid

def isSplittable(towels, design, validDesigns, invalidDesigns):
    if design in towels or design in validDesigns:
        return True
    elif design not in towels and len(design) == 0:
        return False
    elif design in invalidDesigns:
        return False
    else:
        for i in range(1,len(design)):
            #print(design[:i],design[i:])
            isSplitLeft = isSplittable(towels, design[:i], validDesigns, invalidDesigns)
            #print(isSplitLeft)
            if isSplitLeft and design[:i] not in validDesigns:
                validDesigns.append(design[:i])
            elif not isSplitLeft and design[:i] not in invalidDesigns:
                invalidDesigns.append(design[:i])

            isSplitRight = isSplittable(towels, design[i:], validDesigns, invalidDesigns)
            #print(isSplitRight)
            if isSplitRight and design[i:] not in validDesigns:
                validDesigns.append(design[i:])
            elif not isSplitRight and design[i:] not in invalidDesigns:
                invalidDesigns.append(design[i:])

            if isSplitLeft and isSplitRight:
                return True
            
        return False

def solve(input_file):
    towels, designs = read_datas(input_file)
    validDesigns = []
    invalidDesigns = []
    count = 0
    for design in designs:
        print(design)
        #if splitDesign(towels, design):
        if isSplittable(towels, design, validDesigns, invalidDesigns):
            count += 1
    return count

# unit tests
towels_test, designs_test = read_datas("day19_data_test.txt")
validDesigns = []
invalidDesigns = []
assert(isSplittable(towels_test, designs_test[0], validDesigns, invalidDesigns)==True)
assert(isSplittable(towels_test, designs_test[1], validDesigns, invalidDesigns)==True)
assert(isSplittable(towels_test, designs_test[2], validDesigns, invalidDesigns)==True)
assert(isSplittable(towels_test, designs_test[3], validDesigns, invalidDesigns)==True)
assert(isSplittable(towels_test, designs_test[4], validDesigns, invalidDesigns)==False)
assert(isSplittable(towels_test, designs_test[5], validDesigns, invalidDesigns)==True)
assert(isSplittable(towels_test, designs_test[6], validDesigns, invalidDesigns)==True)
assert(isSplittable(towels_test, designs_test[7], validDesigns, invalidDesigns)==False)

print(read_datas("day19_data_test.txt"))
#assert(len(splitDesign(towels_test, designs_test[0]))>0)
#assert(len(splitDesign(towels_test, designs_test[1]))>0)
#assert(len(splitDesign(towels_test, designs_test[2]))>0)
#assert(len(splitDesign(towels_test, designs_test[3]))>0)
#assert(len(splitDesign(towels_test, designs_test[4]))==0)
#assert(len(splitDesign(towels_test, designs_test[5]))>0)
#assert(len(splitDesign(towels_test, designs_test[6]))>0)
#assert(len(splitDesign(towels_test, designs_test[7]))==0)
#assert(solve("day19_data_test.txt")==6)

# print solution
print("Number of possible designs:",solve("day19_data.txt"))