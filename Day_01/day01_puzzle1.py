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

def solve(input_file):
    # read datas
    column_1, column_2 = read_datas(input_file)

    # sort the lists
    column_1.sort()
    column_2.sort()

    # compute and add distances
    distance = 0
    for i in range(0,len(column_1)):
        distance = distance + abs(column_1[i]-column_2[i])

    # return result
    return distance

# unit test
assert(solve("day01_data_test.txt") == 11)

# print result
print("Total distance = ", solve("day01_data.txt"))


