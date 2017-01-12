__author__ = 'nsifniotis'

import csv

unfoundNumbers = []

def _splitOnInterval(interval, string):
    if string == "":
        return []

    results = []

    while len(string) > 0:
        results.append(string[0:interval])
        string = string[interval:]

    return results

def _insertNumber(serialNumber, data):
    global unfoundNumbers
    if serialNumber in data:
        desc, value = data[serialNumber]
        data[serialNumber] = (desc, True)
    else:
        unfoundNumbers.append(number)


with open("data/data.txt", "r") as inputFile:
    dataLines = inputFile.readlines()

with open("data/parts_list.csv", "r") as inputFile:
    csvParser = csv.reader(inputFile)

    parts = dict()
    for line in csvParser:
        serial = line[0]
        desc = line[1]
        found = False
        parts[serial] = (desc, found)

state = 0
for line in dataLines:
    numbers = []
    if state == 0:
        numbers = _splitOnInterval(18, line.strip())
        state = 1
    elif state == 1:
        numbers = _splitOnInterval(10, line.strip())
        state = 0

    for number in numbers:
        _insertNumber(number[-10:], parts)

with open("parts_list_out.csv", "w") as outputFile:
    for key in parts:
        desc, value = parts[key]
        outputFile.write(key + ", \"" + desc + "\", " + ("Found" if value is True else "") + "\n")

with open("unfound.txt", "w") as outputFile:
    for line in unfoundNumbers:
        outputFile.write(line + "\n")
