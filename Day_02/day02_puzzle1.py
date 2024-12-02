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

def isSafe(report):
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

def getNbrSafeReports(input_file):
    # read datas
    reports = read_datas(input_file)
    # compute number of safe reports
    nbr_safe = 0
    for report in reports:
        if (isSafe(report)):
            nbr_safe += 1
    # return number of safe reports
    return nbr_safe

# unit test
assert(getNbrSafeReports("day02_data_test.txt") == 2)
# puzzle result
print("Number of safe reports: ", getNbrSafeReports("day02_data.txt"))