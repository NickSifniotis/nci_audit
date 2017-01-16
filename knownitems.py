__author__ = 'nsifniotis'

from item import Item
import csv


class KnownItems:
    def __init__(self, filename):
        """
        Create this repository from the information stored in filename.
        :param filename: The CSV file containing the list of known serial numbers
        :return: Nothing
        """
        self._parts = dict()
        with open(filename, "r") as inputFile:
            csvParser = csv.reader(inputFile)
            for line in csvParser:
                item = Item()
                item.SetSerialNumber(self._dequote(line[0].strip()))
                if line[1].strip() == "found":
                    item.FindItem()
                if line[2].strip() == "original":
                    item.IsOriginal()
                modelNumber = ",".join(line[3:]).strip()
                item.SetModelNumber(modelNumber)

                self._parts[line[0]] = item


    def Item(self, serialNumber):
        """
        Returns the item associated with a serial number, if it exists, or None if it doesn't.

        :param serialNumber: The serial number to search for.
        :return: The item that owns that serial number, or None if no item owns it.
        """
        res = None
        if serialNumber in self._parts:
            res = self._parts[serialNumber]

        return res


    def AddItem(self, newItem):
        """
        Occasionally the input process results in the creation of a new item, because the serial
        number is not in the list provided by the NCI. When this happens, the item needs to be
        added to this list of known items, or it's data could be lost forever.

        :param newItem: The item to add to the list of known items.
        :return: Nothing.
        """
        serialNumber = newItem.SerialNumber()
        self._parts[serialNumber] = newItem


    def SaveData(self, fileName):
        """
        Saves the current state of data to the CSV file.

        :param fileName: The file to save to.
        :return: Nothing
        """
        with open(fileName, "w") as outputFile:
            for key in self._parts:
                item = self._parts[key]
                outputFile.write(item.SerialNumber() + ",")
                outputFile.write("found" if item.Found() else "not found")
                outputFile.write(",")
                outputFile.write("original" if item.Original() else "not original")
                outputFile.write("," + item.ModelNumber())
                outputFile.write("\n")


    @staticmethod
    def _dequote(s):
        """
        If a string has single or double quotes around it, remove them.
        Make sure the pair of quotes match.
        If a matching pair of quotes is not found, return the string unchanged.
        """
        if s == "":
            return ""

        if (s[0] == s[-1]) and s.startswith(("'", '"')):
            return s[1:-1]
        return s
