import re
import sys
import numpy as np

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
    program_char = getOutput(program)
    registers[0] = 0
    program_output = computeOutput(program, registers)
    A_base8 = '1' + '0'*(len(program)-1)
    registers[0] = [int(A_base8,base=8)]
    for i in range(0,len(program)):
        # compute the value of each byte
        j = 0
        while j < 8 and program[-1-i] != int(program_output[-1-2*i]):
            A_base8 = A_base8[:i] + str(j) + A_base8[i+1:]
            registers[0] = int(A_base8, base=8)
            registers[1] = 0
            registers[2] = 0
            program_output = computeOutput(program, registers)
            j += 1
            #print("base 8:", A_base8, "int:", int(A_base8,base=8), "output:", program_output)
    # let finish with a reduced brute force...
    initA = int(A_base8,base=8)-1
    while (program_char != program_output):
        initA += 1
        registers[0] = initA
        registers[1] = 0
        registers[2] = 0
        program_output = computeOutput(program, registers)
    return initA


# unit tests
registers_test, program_test = read_datas("day17_data_test.txt")
#assert(solve("day17_data_test2.txt")==117440)

# print result
print("Output values:",solve("day17_data.txt"))