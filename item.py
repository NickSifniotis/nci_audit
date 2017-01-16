__author__ = 'nsifniotis'


class Item:
    def __init__(self):
        """
        Constructs a new item. Items are things with serial numbers and other
        assorted bits of information.
        :return: Nothing.
        """
        self._serialNumber = ""
        self._modelNumber = ""
        self._found = False
        self._original = False


    def __repr__(self):
        res =  self._serialNumber + ": \"" + self._modelNumber + "\""
        if self._found:
            res += " (found)"
        return res


    def SerialNumber(self):
        return self._serialNumber


    def ModelNumber(self):
        return self._modelNumber


    def Found(self):
        return self._found


    def Original(self):
        return self._original


    def SetSerialNumber(self, serialNumber):
        self._serialNumber = serialNumber


    def SetModelNumber(self, modelNumber):
        self._modelNumber = modelNumber


    def FindItem(self):
        self._found = True


    def IsOriginal(self):
        self._original = True
