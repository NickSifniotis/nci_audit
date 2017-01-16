__author__ = 'nsifniotis'

from item import Item
from knownitems import KnownItems


class Shelf:
    def __init__(self, knownItems):
        """
        Construct a new shelf - these things contain both racks and storage.
        :return: Nothing. Wtf. This is a constructor.
        """
        self._storage = set()
        self._blades = set()

        self._knownItems = knownItems


    def __str__(self):
        """
        Returns a pretty representation of this shelf.
        :return:
        """
        res = []
        res.append("Shelf")
        res.append("Storage Units:")
        for storage in self._storage:
            res.append(str(storage))
        res.append("Blades:")
        for blade in self._blades:
            res.append(str(blade))
        return "\n".join(res)


    def AddBlade(self, serialNumber):
        """
        Adds a blade server with the given serial number to the set owned by this shelf.
        If the serial number is recognised, this work is easy.
        If it's not recognised, prompt the user for the model number.
        :param serialNumber: The serian number that has been read from the input device.
        :return: Nothing.
        """
        self._addItem(serialNumber, self._blades)


    def AddStorage(self, serialNumber):
        """
        As per the function above, but with storage units instead of blades.

        :param serialNumber: The serial number that has been read from the input device.
        :return: Nothing
        """
        self._addItem(serialNumber, self._storage)


    def SaveShelf(self, fileHandle):
        """
        Saves this shelf to disk.

        :param fileHandle:
        :return:
        """
        storageString = ":".join(s.SerialNumber() for s in self._storage)
        bladeString = ":".join(s.SerialNumber() for s in self._blades)

        fileHandle.write("SHELF\n")
        fileHandle.write("STORAGE:" + storageString + "\n")
        fileHandle.write("BLADE:" + bladeString + "\n")


    def _addItem(self, serialNumber, dataSet):
        """
        Adds an item to the given dataset. If not found, prompts the user for the model number
        and creates a new item. This new item is then added back to the Known Items store.

        :param serialNumber:
        :param dataSet:
        :return:
        """
        item = self._knownItems.Item(serialNumber)
        if item is None:
            modelNumber = input("Model not matched, enter model number: ")
            item = Item()
            item.SetSerialNumber(serialNumber)
            item.SetModelNumber(modelNumber)
            self._knownItems.AddItem(item)
        else:
            print (serialNumber + " matched.")

        item.FindItem()
        dataSet.add(item)


class Rack:
    def __init__(self, name, knownItems):
        """
        Creates a new rack object.

        :param name: The name of the rack.
        :return:
        """
        self._name = name
        self._knownItems = knownItems
        self._shelves = []


    def __str__(self):
        """
        Returns a pretty stringy version of this rack.

        :return:
        """
        res = []
        res.append ("Rack " + self._name)
        for shelf in self._shelves:
            res.append(str(shelf))

        return "\n".join(res)


    def CreateNewShelf(self):
        """
        Creates a new shelf to sit on this rack - and returns a reference to it.
        :return:
        """
        shelf = Shelf(self._knownItems)
        self._shelves.append(shelf)
        return shelf


    def SaveRack(self, fileHandle):
        """
        Saves the data stored in this rack to the filehandle provided.

        :param fileHandle: The file to save the data into.
        :return:
        """
        fileHandle.write("RACK\n")
        fileHandle.write("NAME:" + self._name + "\n")
        for shelf in self._shelves:
            shelf.SaveShelf(fileHandle)
