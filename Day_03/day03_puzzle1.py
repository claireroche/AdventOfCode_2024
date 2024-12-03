def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # reading the file 
    data = my_file.read()
    # store each character in a list
    memory = []
    for char in data:
        memory.append(char)
    # closing file
    my_file.close()
    # return the list
    return memory

def concatenateNumbers(memory):
    """
    This function aims to concatenate adjacent numbers of the memory list
    into the same char.
    """
    conc_memory = []
    index = 0
    while (index < len(memory)):
        char = memory[index]
        # let the non-digit char alone in the new list
        if (not char.isdigit()):
            conc_memory.append(char)
            index += 1
        # detect sequences of adjacent char digits,
        # and concatenate them into one char in the new list
        else:
            char_number = char
            char = memory[index+1]
            char_lenght = 1
            while (char.isdigit()):
                char_number += char
                char_lenght += 1
                char = memory[index+char_lenght]
            conc_memory.append(char_number)
            index += char_lenght

    # return the concatenated list
    return conc_memory

def isValidOperation(sequence):
    """
    This function returns, for a sequence, if its format is valid or not.
    If it is valid, it also returns the mult result.
    """
    isValid = True
    result = 0
    # back-up check: in solve, we only pass sequences of lenght equal to 8
    if (len(sequence) != 8):
        return False, 0
    # back-up check: in solve, we only pass sequences that starts by char 'm'
    if (sequence[0] != 'm'):
        return False, 0
    if (sequence[1] != 'u'):
        return False, 0
    if (sequence[2] != 'l'):
        return False, 0
    if (sequence[3] != '('):
        return False, 0
    if (sequence[5] != ','):
        return False, 0
    if (sequence[7] != ')'):
        return False, 0
    if (not sequence[4].isdigit() or not sequence[6].isdigit()):
        return False, 0
    # if the sequence pass the format checks,
    # then we can compute the mult result and return it
    result = int(sequence[4])*int(sequence[6])
    
    return isValid, result

def solve(input_file):
    # read input datas
    memory = read_datas(input_file)
    # concatane adjacent numbers into same chars
    conc_memory = concatenateNumbers(memory)
    # result init
    sum = 0
    index = 0
    while (index < len(conc_memory)-8):
        # if we spot a "m", we check the 8-characters sequence
        if (conc_memory[index] == 'm'):
            isValid, mult = isValidOperation(conc_memory[index:index+8])
            if (isValid):
                sum += mult
                # if the sequence is valid, we can skip the check of the 7 next chars
                index += 7
            else:
                index += 1
        else:
            index += 1

    return sum


memory = read_datas("day03_data_test.txt")
# unit test
assert(solve("day03_data_test.txt") == 161)
# puzzle result
print("All multiplications sum: ", solve("day03_data.txt"))

