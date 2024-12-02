def read_datas(input_file):
    # open file
    my_file = open(input_file)
    # read lines
    data = my_file.readlines()
    # create reports
    reports = []
    for line in data:
        # create report
        reports.append([int(nbr) for nbr in line.split(" ")])
    # closing file
    my_file.close()

    return reports

def isSafeReport(report):
    is_safe = True
    order = report[1]-report[0]
    for i in range(0,len(report)-1):
        diff = report[i+1]-report[i]
        # check the difference between two adjacent numbers
        if (abs(diff) < 1 or abs(diff) > 3):
            return False
        # check the order, with the difference between the two first elements as reference.
        # of course, this check is useless for i=0.
        if ( order*diff < 0 ):
            return False
    return is_safe

def isSafeWithRemovedLevel(report):
    """ 
    This function takes a report as an input.
    It aims to check if, by removing one level
    at a time of this report, it becomes safe
    or not, according to the first definition.
    If it finds a safe solution, it returns
    true without going through the remaining
    possibilities.
    """
    isSafe = False
    level_index = 0     # index of the removed level
    while ((not isSafe) and level_index < len(report)):
        # create a copy of the report
        report_tmp = report.copy()
        # remove a level from the report
        report_tmp.pop(level_index)
        # check if the report is safe
        isSafe = isSafeReport(report_tmp)
        # if it is not safe, we check other possibilities
        if (not isSafe):
            level_index += 1
    return isSafe

def getNbrSafeReports(input_file):
    # read datas
    reports = read_datas(input_file)
    # compute number of safe reports
    nbr_safe = 0
    for report in reports:
        if (isSafeReport(report)):
            nbr_safe += 1
        elif (isSafeWithRemovedLevel(report)):
            nbr_safe += 1
    # return number of safe reports
    return nbr_safe

# unit test
assert(getNbrSafeReports("day02_data_test.txt") == 4)
# puzzle result
print("Number of safe reports: ", getNbrSafeReports("day02_data.txt"))