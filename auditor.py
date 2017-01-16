__author__ = 'nsifniotis'

from rack import Rack
from knownitems import KnownItems


def _displayCommands():
    print("Commands:")
    print("0: Quit")
    print("1. New Rack")
    print("2. New Shelf")
    print("3. Scan blades")
    print("4. Scan storage")


def _splitOnInterval(interval, string):
    if string == "":
        return []

    results = []

    while len(string) > 0:
        results.append(string[0:interval])
        string = string[interval:]

    return results


def _scanBlades(currentShelf):
    finished = False
    while not finished:
        serialNumber = input().strip()
        if serialNumber == "0":
            finished = True
        else:
            currentShelf.AddBlade(serialNumber)


def _scanStorage(currentShelf):
    finished = False
    while not finished:
        serialNumber = input().strip()
        if serialNumber == "0":
            finished = True
        else:
            currentShelf.AddStorage(serialNumber)


knownItems = KnownItems("data/parts_list.csv")


knownItems.SaveData("data/parts_list.csv")
exit(0)

with open("data/racks.txt", "r") as inputFile:
    dataLines = inputFile.readlines()

racks = []
currentRack = None
currentShelf = None
state = 0
for line in dataLines:
    lineParts = line.strip().split(":")
    command = lineParts[0]

    if command == "RACK":
        if currentRack is not None:
            racks.append(currentRack)
        state = 1

    elif command == "NAME" or command == "name":
        if state is 1:
            name = lineParts[1]
            currentRack = Rack(name, knownItems)
            state = 2
        else:
            raise Exception("Bad state in rack load function.")

    elif command == "SHELF":
        currentShelf = currentRack.CreateNewShelf()

    elif command == "STORAGE":
        for serialNumber in lineParts[1:]:
            currentShelf.AddStorage(serialNumber)

    elif command == "BLADE":
        for serialNumber in lineParts[1:]:
            currentShelf.AddBlade(serialNumber)


done = False
currentRack = None
currentShelf = None
while not done:
    _displayCommands()
    instruction = input("Next command:").strip()

    if instruction == "0":
        done = True
    elif instruction == "1":
        # create a new rack
        rackName = input("New rack name: ")
        currentRack = Rack(rackName, knownItems)
        racks.append(currentRack)
    elif instruction == "2":
        # create a new shelf for an existing rack
        if currentRack is not None:
            currentShelf = currentRack.CreateNewShelf()
        else:
            print("No rack selected.")
    elif instruction == "3":
        # scan some blade servers
        if currentShelf is not None:
            _scanBlades(currentShelf)
        else:
            print ("Unable to scan blades, no shelf created.")
    elif instruction == "4":
        # scan some storage units
        if currentShelf is not None:
            _scanStorage(currentShelf)
        else:
            print ("Unable to scan storage, no shelf created.")
    else:
        print("Unrecognised command.")



knownItems.SaveData("data/parts_list.csv")

with open("data/racks.txt", "w") as outputFile:
    for rack in racks:
        rack.SaveRack(outputFile)
