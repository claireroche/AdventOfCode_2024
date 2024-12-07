import numpy as np

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
    Here, we write the int comb_index using base-3 representation
    with size bits. Each bit will correspond to
    a +, a *, or || (concatenate) operation.
    """
    b = np.base_repr(comb_index,3)
    operations = [0]*size
    for i in range (1,len(b)+1):
        operations[-i] = int(b[-i])
    return operations

def concatenateNumbers(n, m):
    return int(str(n)+str(m))

def getEquationResult(numbers, operators):
    """
    Given a list of numbers, and the operators sequence,
    we return the equation result. Here, we assume that '0'
    stands for a +, while '1' stands for *, and '2' is for
    concatenate operator.
    """
    res = numbers[0]
    for i in range(0, len(operators)):
        if (operators[i]==0):
            res = res + numbers[i+1]
        elif (operators[i]==1):
            res = res*numbers[i+1]
        elif (operators[i]==2):
            res = concatenateNumbers(res, numbers[i+1])
        else:
            print("getEquationResults: unknown operator.")
    return res

def isValidCalibration(result, numbers):
    """
    Here, we test all the operators combinations until
    at least one valid one is found. To do so, we use
    the base-3 representation.
    The right part of the equation contains n numbers,
    so we're supposed to have (n-1) operators.
    An operation can be a + (0 in our case), a * (1 here), 
    or a concatenate operation || (3 here).
    We have 3**(n-1) possible combinations.
    """
    isValid = False
    comb_index = 0
    # we stop when a valid combination is found
    while (not isValid and comb_index < 3**(len(numbers)-1)):
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
assert(getOperations(3,9)==[1,0,0])
assert(getOperations(4,10)==[0,1,0,1])
assert(concatenateNumbers(10,1)==101)
assert(concatenateNumbers(34,29)==3429)
assert(isValidCalibration(calibrations_test[0][0], calibrations_test[0][1])==True)
assert(isValidCalibration(calibrations_test[8][0], calibrations_test[8][1])==True)
assert(isValidCalibration(calibrations_test[1][0], calibrations_test[1][1])==True)
assert(isValidCalibration(calibrations_test[6][0], calibrations_test[6][1])==True)
assert(isValidCalibration(calibrations_test[4][0], calibrations_test[4][1])==True)
assert(isValidCalibration(calibrations_test[2][0], calibrations_test[2][1])==False)
assert(solve("day07_data_test.txt")==11387)
# solve
print("Total calibration result:", solve("day07_data.txt"))