def read_datas(input_file):
    # opening the file in read mode 
    my_file = open(input_file) 
    # reading the file 
    data = my_file.readlines()
    # separate the rules and updates in different lists
    rules = []
    updates = []
    for line in data:
        line = line.strip()
        if (line.count('|')):
            rule = []
            rule.append(int(line.split('|')[0]))
            rule.append(int(line.split('|')[1]))
            rules.append(rule)
        elif (len(line)):
            update = []
            for i in range(0,len(line.split(','))):
                update.append(int(line.split(',')[i]))
            updates.append(update)
    # closing file
    my_file.close()
    # return the lists
    return rules, updates

def isValidOrder(rules, page1, page2):
    if [page1,page2] in rules:
        return True
    elif [page2,page1] in rules:
        return False
    else:
        print("isValidOrder: un-specified rule.")
        return False

def isValidUpdate(rules, update):
    for i in range(0,len(update)-1):
        for j in range(i+1,len(update)):
            if (not isValidOrder(rules, update[i], update[j])):
                return False
    return True

def reOrderUpdate(rules, update):
    isOrdered = False
    while (not isOrdered):
        for i in range(0,len(update)-1):
            for j in range(i+1,len(update)):
                if (not isValidOrder(rules, update[i], update[j])):
                    update[i], update[j] = update[j], update[i]
        isOrdered = isValidUpdate(rules, update)
    return update

def solve(input_file):
    # read input datas
    rules, updates = read_datas(input_file)
    # init sum
    sum = 0
    for update in updates:
        if (not isValidUpdate(rules, update)):
            update = reOrderUpdate(rules, update)
            sum += update[int(len(update)/2)]
    return sum

# unit tests
rules_test, updates_test = read_datas("day05_data_test.txt")
assert(isValidOrder(rules_test,29,13)==True)
assert(isValidOrder(rules_test,53,97)==False)
assert(isValidOrder(rules_test,29,47)==False)
assert(isValidUpdate(rules_test, updates_test[0])==True)
assert(isValidUpdate(rules_test, updates_test[3])==False)
assert(isValidUpdate(rules_test, updates_test[4])==False)
assert(isValidUpdate(rules_test, updates_test[5])==False)
update = reOrderUpdate(rules_test, updates_test[3])
assert(isValidUpdate(rules_test, update)==True)
update = reOrderUpdate(rules_test, updates_test[4])
assert(isValidUpdate(rules_test, update)==True)
assert(solve("day05_data_test.txt")==123)

# print result
print("Middle page sum of correctly-ordered updates:", solve("day05_data.txt"))