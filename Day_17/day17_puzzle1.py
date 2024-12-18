import re
import sys

def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.readlines()
    # fill the registers
    registers = []
    line_registerA = datas[0].strip()
    line_registerB = datas[1].strip()
    line_registerC = datas[2].strip()
    registers.append(int(re.findall(r'\d+', line_registerA)[0]))
    registers.append(int(re.findall(r'\d+', line_registerB)[0]))
    registers.append(int(re.findall(r'\d+', line_registerC)[0]))
    program = []
    line_program = datas[4].strip()
    p = re.findall(r'\d+', line_program)
    for i in p:
        program.append(int(i))
    # closing file
    my_file.close()
    # return the list
    return registers, program

def getCombo(registers, operand):
    combo = 0
    if operand < 4:
       combo = operand
    elif operand == 4:
        combo = registers[0]
    elif operand == 5:
        combo = registers[1]
    elif operand == 6:
        combo = registers[2]
    elif operand == 7:
        print("getCombo: error.")
    return combo 

def adv(registers, operand):
    registers[0] = int(registers[0]/(2**getCombo(registers,operand)))
    return registers

def bxl(registers, operand):
    registers[1] = registers[1]^operand
    return registers

def bst(registers, operand):
    registers[1] = getCombo(registers, operand)%8
    return registers

def jnz(registers, operand, instructionPointer):
    if registers[0] == 0:
        return registers, instructionPointer+2
    else:
        return registers, operand

def bxc(registers, operand):
    registers[1] = registers[1]^registers[2]
    return registers

def out(registers, operand, outPut):
    outPut.append(getCombo(registers, operand)%8)
    return registers, outPut

def bdv(registers, operand):
    registers[1] = int(registers[0]/(2**getCombo(registers,operand)))
    return registers

def cdv(registers, operand):
    registers[2] = int(registers[0]/(2**getCombo(registers,operand)))
    return registers

def getOutput(outPut):
    char = str(outPut[0])
    for i in range(1,len(outPut)):
        char += ',' + str(outPut[i])
    return char

def computeOutput(program, registers):
    output = []
    instructionPointer = 0
    while instructionPointer < len(program)-1:
        if program[instructionPointer] == 0:
            registers = adv(registers, program[instructionPointer+1])
            instructionPointer += 2
        elif program[instructionPointer] == 1:
            registers = bxl(registers, program[instructionPointer+1])
            instructionPointer += 2
        elif program[instructionPointer] == 2:
            registers = bst(registers, program[instructionPointer+1])
            instructionPointer += 2
        elif program[instructionPointer] == 3:
            registers, instructionPointer = jnz(registers, program[instructionPointer+1], instructionPointer)
        elif program[instructionPointer] == 4:
            registers = bxc(registers, program[instructionPointer+1])
            instructionPointer += 2
        elif program[instructionPointer] == 5:
            registers, output = out(registers, program[instructionPointer+1], output)
            instructionPointer += 2
        elif program[instructionPointer] == 6:
            registers = bvd(registers, program[instructionPointer+1])
            instructionPointer += 2
        elif program[instructionPointer] == 7:
            registers = cdv(registers, program[instructionPointer+1])
            instructionPointer += 2
    return getOutput(output)

def solve(input_file):
    registers, program = read_datas(input_file)
    return computeOutput(program, registers)


# unit tests
assert(bst([0,0,9],6)[1]==1)
assert(bxl([0,29,0],7)[1]==26)
assert(bxc([0,2024,43690],0)[1]==44354)
registers_test, program_test = read_datas("day17_data_test.txt")
print(registers_test)
print(program_test)
assert(solve("day17_data_test.txt")=='4,6,3,5,6,3,5,2,1,0')
assert(computeOutput([0,1,5,4,3,0],[2024,0,0])=='4,2,5,6,7,7,7,7,3,1,0')
print(solve("day17_data_test2.txt"))

# print result
print("Output values:",solve("day17_data.txt"))
