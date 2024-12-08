def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # reading the file 
    data = my_file.readlines()
    # create the map
    map = []
    for line in data:
        line = line.strip()
        line_list = []
        for char in line:
            line_list.append(char)
        map.append(line_list)
    # closing file
    my_file.close()
    # return the map
    return map

def isInMap(map, cell):
    """
    Return True if cell [i,j] is in map. False otherwise.
    """
    return (cell[0] >= 0 and cell[0] < len(map) and cell[1] >= 0 and cell[1] < len(map[cell[0]]))

def getSymmetricPosition(cell1, cell2):
    """
    Get symmetric cell of cell2, according to cell1.
    """
    di = cell2[0]-cell1[0]
    dj = cell2[1]-cell1[1]
    return [cell1[0]-di, cell1[1]-dj]

def updateSortedAntennas(sorted_antennas, antenna_frequency, i, j):
    """
    Update the sorted map of antennas according to their frequency,
    to add a new antenna. If an entry of antennas corresponding to
    this frequency already exists, we update this list. If it does
    not exist, we create this new list, corresponding to this new
    frequency.
    """
    # if the antenna frequency already exist in the list,
    # we update the list of positions
    if (antenna_frequency in sorted_antennas[0]):
        frequency_index = sorted_antennas[0].index(antenna_frequency)
        sorted_antennas[1][frequency_index].append([i,j])
    # if this is the first antenna of this frequency found,
    # we create the entry in the sorted list
    else:
        sorted_antennas[0].append(antenna_frequency)
        sorted_antennas[1].append([[i,j]])
    return sorted_antennas

def sortAntennasByFrenquencies(map):
    """
    Sort the antenna found on the map by frequencies.
    For each frequency, we store the list of positions
    of antennas of this frequency.
    """
    sorted_antennas = [[],[]]
    for i in range(0,len(map)):
        for j in range(0,len(map[i])):
            # if there is an antenna on cell (i,j) of the map
            if (map[i][j] != '.'):
                # get the antenna frequency
                antenna_frequency = map[i][j]
                # sort the antenna in the sorted list
                updateSortedAntennas(sorted_antennas, antenna_frequency, i, j)
    return sorted_antennas

def addAntennaAntinodeCells(map, sorted_antennas, frequency, antenna, antinodeCells):
    """
    For a given antenna of frequency, return all its antinode cells.
    """
    newAntinodeCells = antinodeCells.copy()
    frequency_index = sorted_antennas[0].index(frequency)
    antenna_index = sorted_antennas[1][frequency_index].index(antenna)
    # for each antenna_k of the same frequency as input antenna,
    # compute the corresponding antinode created by antenna.
    for k in range(0, len(sorted_antennas[1][frequency_index])):
        antenna_k = sorted_antennas[1][frequency_index][k]
        if (antenna_k != antenna):
            cell_2 = getSymmetricPosition(antenna, antenna_k)
            # we compute only antinodes in the map.
            # also, the we compute the uniq antinodes position
            cell_0 = antenna_k.copy()
            cell_1 = antenna.copy()
            # propagate the pattern to get all the antinodes,
            # until we go out of the map bounds
            while (isInMap(map, cell_2)):
                if (not cell_2 in newAntinodeCells):
                    newAntinodeCells.append(cell_2)
                cell_2 = getSymmetricPosition(cell_1, cell_0)
                cell_0 = cell_1.copy()
                cell_1 = cell_2.copy()
    return newAntinodeCells

def addFrequencyAntinodeCells(map, sorted_antennas, frequency, antinodeCells):
    """
    For a given frequency, add all the antinodes created by all the antennas
    of this given frequency.
    """
    newAntinodeCells = antinodeCells.copy()
    frequency_index = sorted_antennas[0].index(frequency)
    for j in range(0, len(sorted_antennas[1][frequency_index])):
        antenna_j = sorted_antennas[1][frequency_index][j]
        # for each antenna of the frequency, add the new antinode cells
        newAntinodeCells = addAntennaAntinodeCells(map, sorted_antennas, frequency, antenna_j, newAntinodeCells)
    return newAntinodeCells

def getAntinodeCells(map, sorted_antennas):
    """
    Get all the antinode cells, for all the antennas of
    all the frequencies.
    """
    antinodeCells = []
    for i in range (0, len(sorted_antennas[0])):
        # add all the antinode of this frequency
        antinodeCells = addFrequencyAntinodeCells(map, sorted_antennas, sorted_antennas[0][i], antinodeCells)
        # if there is more than one antenna in the frequency set,
        # we also have one antinode per antenna
        if (len(sorted_antennas[1][i])>=2):
            for antenna in sorted_antennas[1][i]:
                if (not antenna in antinodeCells):
                    antinodeCells.append(antenna)
    return antinodeCells

def solve(input_file):
    # read inputs
    map_antennas = read_datas(input_file)
    # sort the antennas positions by frequencies
    sortedAntennas = sortAntennasByFrenquencies(map_antennas)
    # compute number of antinodes
    antinodeCells = getAntinodeCells(map_antennas, sortedAntennas)
    # return number of uniq locations
    return len(antinodeCells)

# unit tests
map_test = read_datas("day08_data_test.txt")
assert(isInMap(map_test, [0,0])==True)
assert(isInMap(map_test, [12,2])==False)
assert(isInMap(map_test, [5,-2])==False)
sortedAntennas_test = sortAntennasByFrenquencies(map_test)
assert(len(sortedAntennas_test[0])==2)
assert(len(sortedAntennas_test[1])==2)
assert(sortedAntennas_test[0][0]=='0')
assert(len(sortedAntennas_test[1][0])==4)
assert(sortedAntennas_test[0][1]=='A')
assert(len(sortedAntennas_test[1][1])==3)
assert(getSymmetricPosition([0,0], [3,1])==[-3,-1])
assert(getSymmetricPosition([0,0], [-1,4])==[1,-4])
assert(getSymmetricPosition([2,3], [1,1])==[3,5])
assert(solve("day08_data_test.txt")==34)

# solve puzzle
print("Number of uniq locations of antinodes within the bounds:", solve("day08_data.txt"))