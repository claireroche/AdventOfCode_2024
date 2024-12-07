def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # reading the file 
    data = my_file.readlines()
    # separate each calibration line as follow:
    # [expected result, list_of_right_side_numbers]
    calibrations = []
    for line in data:
        line = line.strip()
        equation = [int(line.split(': ')[0]), []]
        line = line.split(': ')[1].split(' ')
        for char in line:
            equation[1].append(int(char))
        calibrations.append(equation)
    # closing file
    my_file.close()
    # return the calibrations list
    return calibrations

def getOperations(size, comb_index):
    """
    Here, we write the int comb_index using binary
    with size bits. Each bit will correspond to
    a + or * operation.
    """
    b = bin(comb_index)
    b = b.split('b')[1]
    operations = [0]*size
    for i in range (1,len(b)+1):
        operations[-i] = int(b[-i])
    return operations

def getEquationResult(numbers, operators):
    """
    Given a list of numbers, and a the operators sequence,
    we return the equation result. Here, we assume that '0'
    stands for a +, while '1' stands for *.
    """
    res = numbers[0]
    for i in range(0, len(operators)):
        if (operators[i]==0):
            res = res + numbers[i+1]
        elif (operators[i]==1):
            res = res*numbers[i+1]
        else:
            print("getEquationResults: unknown operator.")
    return res

def isValidCalibration(result, numbers):
    """
    Here, we test all the operators combinations until
    at least one valid one is found. To do so, we use
    the binary representation.
    The right part of the equation contains n numbers,
    so we're supposed to have (n-1) operators.
    An operation can be a + (0 in our case), or a * (1 here).
    We have 2**(n-1) possible combinations.
    """
    isValid = False
    comb_index = 0
    # we stop when a valid combination is found
    while (not isValid and comb_index < 2**(len(numbers)-1)):
        operators = getOperations(len(numbers)-1, comb_index)
        isValid = (result == getEquationResult(numbers, operators))
        comb_index += 1
    return isValid

def solve(input_datas):
    calibrations = read_datas(input_datas)
    sum = 0
    for calibration in calibrations:
        if (isValidCalibration(calibration[0], calibration[1])):
            sum += calibration[0]
    return sum

# unit tests
calibrations_test = read_datas("day07_data_test.txt")
assert(getOperations(2,1)==[0,1])
assert(getOperations(2,1)==[0,1])
assert(isValidCalibration(calibrations_test[0][0], calibrations_test[0][1])==True)
assert(isValidCalibration(calibrations_test[8][0], calibrations_test[8][1])==True)
assert(isValidCalibration(calibrations_test[1][0], calibrations_test[1][1])==True)
assert(isValidCalibration(calibrations_test[2][0], calibrations_test[2][1])==False)
assert(solve("day07_data_test.txt")==3749)
# solve
print("Total calibration result:", solve("day07_data.txt"))