def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 

    # reading the file 
    data = my_file.readlines()

    # separate the two columns
    column_1 = []
    column_2 = []

    for line in data:
        column_1.append(int(line.split('   ')[0]))
        column_2.append(int(line.split('   ')[1]))

    # closing file
    my_file.close()

    # return the lists
    return column_1, column_2

def solve_naive(input_file):
    # read datas
    column_1, column_2 = read_datas(input_file)

    # compute and add similarity score
    similarity_score = 0
    for i in range(0,len(column_1)):
        occurency = 0
        for j in range(0,len(column_2)):
            if (column_1[i] == column_2[j]):
                occurency = occurency + 1
        similarity_score = similarity_score + column_1[i]*occurency
    return similarity_score

def solve(input_file):
    # read datas
    column_1, column_2 = read_datas(input_file)

    # compute occurency using a map
    occurency = {}
    for nbr in column_2:
        if nbr not in occurency:
            occurency[nbr] = 0
        occurency[nbr] += 1
        
    # compute similarity score
    similarity_score = 0
    for nbr in column_1:
        if nbr in occurency:
            similarity_score += nbr*occurency[nbr]
    return similarity_score

# unit test: naive solve version
assert(solve_naive("day01_data_test.txt") == 31)

# print result: naive solve version
print("Similarity Score (naive version) = ", solve_naive("day01_data.txt"))

# unit test solve
assert(solve("day01_data_test.txt") == 31)

# print result solve
print("Similarity Score = ", solve("day01_data.txt"))
