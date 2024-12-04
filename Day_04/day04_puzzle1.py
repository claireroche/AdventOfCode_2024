import re

def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # reading the file line by line
    data = my_file.readlines()
    # store each character in a list
    word_search = []
    for line in data:
        line = line.rstrip('\n')
        word_search.append(line)
    # closing file
    my_file.close()
    # return the list
    return word_search

def buildColumnLine(word_search,j):
    """
    Return column concatenated into a single char.
    Here, j gives the index column to build the column char.
        . . . a . . .
        . . . b . . .
    M = . . . c . . .
        . . . d . . .
        . . . e . . .
    buildColumnLine(M,3) would return 'abcde'.
    """
    if (j < 0 or j > len(word_search[0])):
        print("buildDiagLine: Attention, half diag is built.")
    line = ''
    for i in range(0,len(word_search)):
        line += word_search[i][j]
    return line

def buildDiagLine(word_search,i,j):
    """
    Return diagonal concatenated into a single char.
    Here, i and j give the starting index to build the diagonal char.
        . . . a . . .
        . . . . b . .
    M = . . . . . c .
        . . . . . . d
        . . . . . . .
    buildDiagLine(M,0,3) would return 'abcd'.
    We suppose here that all lines have the same length.
    """
    if (i != 0 and j != 0):
        print("buildDiagLine: Attention, half diag is built.")
    line = ''
    while (i < len(word_search) and j < len(word_search[0])):
        line += word_search[i][j]
        i += 1
        j += 1
    return line

def buildBackwardDiagLine(word_search,i,j):
    """
    Return "backward" diagonal concatenated into a single char.
    Here, i and j give the starting index to build the diagonal char.
        . . . a . . .
        . . b . . . .
    M = . c . . . . .
        d . . . . . .
        . . . . . . .
    buildBackwardDiagLine(M,0,3) would return 'abcd'.
    We suppose here that all lines of M have the same length.
    """
    if (i != 0 and j != len(word_search[0])-1):
        print("buildBackwardDiagLine: Attention, half diag is built.")
    line = ''
    while (i < len(word_search) and j >= 0):
        line += word_search[i][j]
        i += 1
        j -= 1
    return line

def nbrXMASinLine(line):
    """
    Use regex to find the occurence of 'XMAS' sequence, and its backward in the input line.
    """
    sum = 0
    for xmas in re.findall(r'XMAS',line):
        sum += 1
    for samx in re.findall(r'SAMX',line):
        sum += 1
    return sum

def solve(input_file):
    # read input file
    word_search = read_datas(input_file)
    # get nbr lines and columns (we assume here that all lines have same number of columns)
    Nx = len(word_search)
    Ny = len(word_search[0])
    # init the count number
    sum = 0
    # count number of XMAS and SAMX on lines
    for line in word_search:
        sum += nbrXMASinLine(line)
    # add to count number of XMAS and SAMX on columns
    for j in range(0,Ny):
        line = buildColumnLine(word_search,j)
        sum += nbrXMASinLine(line)
    # add to count the number of XMAS and SAMX on upper diagonals
    # here, we can skip the 3 last diagonals are they are too short to contain XMAS
    for j in range(0,Ny-3): 
        line = buildDiagLine(word_search,0,j)
        sum += nbrXMASinLine(line)
    # add to count the number of XMAS and SAMX on bottom diagonals
    # here, we can skip the 3 last diagonals are they are too short to contain XMAS
    # we also start from 1, as the middle diagonal was already computed before
    for i in range(1,Nx-3):
        line = buildDiagLine(word_search,i,0)
        sum += nbrXMASinLine(line)
    # add to count the number of XMAS and SAMX on upper backward diagonals
    # here, we can skip the 3 last diagonals are they are too short to contain XMAS
    for j in range(3,Ny):  
        line = buildBackwardDiagLine(word_search,0,j)
        sum += nbrXMASinLine(line)
    # add to count the number of XMAS and SAMX on bottom backward diagonals
    # here, we can skip the 3 last diagonals are they are too short to contain XMAS
    for i in range(1,Nx-3):
        line = buildBackwardDiagLine(word_search,i,Ny-1)
        sum += nbrXMASinLine(line)
    # return the sum
    return sum

# unit tests
word_search_test = read_datas("day04_data_test.txt")
assert(nbrXMASinLine(word_search_test[1])==1)
assert(nbrXMASinLine(word_search_test[4])==2)
assert(nbrXMASinLine(word_search_test[9])==1)
assert(buildDiagLine(word_search_test,0,2)=='MMXSXASA')
assert(buildDiagLine(word_search_test,6,0)=='SAMX')
assert(buildBackwardDiagLine(word_search_test,0,2)=='MSA')
assert(buildBackwardDiagLine(word_search_test,0,4)=='XMXSX')
assert(buildBackwardDiagLine(word_search_test,4,len(word_search_test[0])-1)=='MMXSXA')
assert(buildBackwardDiagLine(word_search_test,8,len(word_search_test[0])-1)=='MS')
assert(buildColumnLine(word_search_test,9)=='MAMXMASAMX')
assert(solve("day04_data_test.txt")==18)

# get solution
print("XMAS appears", solve("day04_data.txt"), "times.")