__author__ = 'nsifniotis'

from rack import Rack
from knownitems import KnownItems


unfoundNumbers = []


def _splitOnInterval(interval, string):
    if string == "":
        return []

    results = []

    while len(string) > 0:
        results.append(string[0:interval])
        string = string[interval:]

    return results


knownItems = KnownItems("data/parts_list.csv")


with open("data/data.txt", "r") as inputFile:
    dataLines = inputFile.readlines()

racks = []
position = 0
while position < len(dataLines):
    rack = Rack(dataLines[position].strip(), knownItems)
    position += 1

    for shelves in range(0, 4):
        shelf = rack.CreateNewShelf()

        numbers = _splitOnInterval(18, dataLines[position].strip())
        position += 1
        for item in numbers:
            shelf.AddStorage(item)

        numbers = _splitOnInterval(10, dataLines[position].strip())
        position += 1
        for item in numbers:
            shelf.AddBlade(item)

    racks.append(rack)

for rack in racks:
    print(str(rack))

knownItems.SaveData("data/parts_list.csv")