import re
import sys

def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # read char by char
    datas = my_file.readlines()
    # fill the rules
    buttonsA = []
    buttonsB = []
    prizes = []
    index = 0
    while (index < len(datas)):
        line_buttonA = datas[index].strip()
        line_buttonB = datas[index+1].strip()
        line_prize   = datas[index+2].strip()
        buttonA = re.findall(r'\d+', line_buttonA)
        buttonB = re.findall(r'\d+', line_buttonB)
        prize   = re.findall(r'\d+', line_prize)
        buttonsA.append([int(buttonA[0]), int(buttonA[1])])
        buttonsB.append([int(buttonB[0]), int(buttonB[1])])
        prizes.append([int(prize[0]), int(prize[1])])
        index += 4
    # closing file
    my_file.close()
    # return the list
    return buttonsA, buttonsB, prizes

def getTokensNbr(moveA, moveB):
    return 3*moveA+moveB

def findMinTokens(buttonA, buttonB, prize):
    """
    Solve an integer 2-equations linear system.
    X position equation: prize[0] = moveA*buttonA[0] + moveB*buttonB[0]
    Y position equation: prize[1] = moveA*buttonA[1] + moveB*buttonB[1]
    """
    isReached = False
    minTokensNbr = sys.maxsize
    if buttonB[0]*buttonA[1]-buttonB[1]*buttonA[0] != 0:
        moveB = int( (prize[0]*buttonA[1] - prize[1]*buttonA[0])/(buttonB[0]*buttonA[1]-buttonB[1]*buttonA[0]) )
        moveA = int( (prize[0]-moveB*buttonB[0])/buttonA[0] )
    else:
        print("Error.")
    x = moveA*buttonA[0] + moveB*buttonB[0]
    y = moveA*buttonA[1] + moveB*buttonB[1]
    # check if we can reach the prize with those values
    if (x == prize[0] and y == prize[1]):
        return True, getTokensNbr(moveA, moveB)
    return isReached, minTokensNbr

def solve(input_file, part):
    # read input datas
    rules_bA, rules_bB, prizes = read_datas(input_file)
    # in case of puzzle part 2, we update prizes pos values
    if part==2:
        for prize in prizes:
            prize[0] += 10000000000000
            prize[1] += 10000000000000
    # init the sum of token needed
    tokenSum = 0
    # on each claw
    for i in range(0,len(prizes)):
        # find a way to reach the prize
        isReached, tokenNbr = findMinTokens(rules_bA[i], rules_bB[i], prizes[i])
        # if we can reach it, we note the tokens needed
        if (isReached):
            tokenSum += tokenNbr
    return tokenSum

# unit tests
rules_bA_test, rules_bB_test, prize_test = read_datas("day13_data_test.txt")
#print(rules_bA_test, rules_bB_test, prize_test)
assert(findMinTokens(rules_bA_test[0], rules_bB_test[0], prize_test[0])==(True,280))
assert(findMinTokens(rules_bA_test[1], rules_bB_test[1], prize_test[1])==(False,sys.maxsize))
assert(solve("day13_data_test.txt",1)==480)

# print solution: part 1
print("Fewest tokens spent to win all possible prizes (Part 1):", solve("day13_data.txt",1))
# print solution: part 2
print("Fewest tokens spent to win all possible prizes (Part 2):", solve("day13_data.txt",2))