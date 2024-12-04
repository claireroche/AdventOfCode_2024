def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # reading the file line by line
    data = my_file.readlines()
    # store each character in a list
    word_search = []
    for line in data:
        line = line.rstrip('\n')
        L = []
        for char in line:
            L.append(char)
        word_search.append(L)
    # closing file
    my_file.close()
    # return the list
    return word_search

def isMAS(sequence):
    if (sequence=="MAS" or sequence=="SAM"):
        return True
    return False

def isXMAS(word_search,i,j):
    isXmas = True
    diag1 = word_search[i-1][j-1] + word_search[i][j] + word_search[i+1][j+1]
    if (not isMAS(diag1)):
        return False
    diag2 = word_search[i-1][j+1] + word_search[i][j] + word_search[i+1][j-1]
    if (not isMAS(diag2)):
        return False
    return isXmas

def solve(input_file):
    # read input datas
    word_search = read_datas(input_file)
    # init sum
    sum = 0
    # we make sure to avoid boundaries
    for i in range(1,len(word_search)-1):
        # we assume here that each line has the same length
        for j in range(1,len(word_search[0])-1):
            if (word_search[i][j] == 'A' and isXMAS(word_search,i,j)):
                sum += 1   
    # return the final sum             
    return sum
    
# unit tests
word_search_test = read_datas("day04_data_test.txt")
assert(solve("day04_data_test.txt")==9)
# get solution
print("There are", solve("day04_data.txt"), "X-MAS.")