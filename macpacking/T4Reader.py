from macpacking.reader import BinppReader, DatasetReader, JBurkardtReader


class T4Reader():
    def __init__(self) -> None:
        self.capacity
        self.temp = []

    # if you want to directly convert file to datasets for RFF
    # this isn't actually needed
    def getData(self, fileType, filePath):
        if fileType == "binpp" or fileType == "binpp-hard":
            reader: DatasetReader = BinppReader(filePath[0])
            self.capacity = reader.offline()[0]
            self.temp = reader.offline()[1]
        elif fileType == "jburkardt":
            reader: DatasetReader = JBurkardtReader(filePath[0], filePath[1])
            self.capacity = reader.offline()[0]
            self.temp = reader.offline()[1]
        sizes = self.normalize(self.capacity, self.temp)
        return sizes

    def normalize(capacity, dataInitial):
        sizes = [[], [], [], [], [], []]
        for weight in dataInitial:
            if weight <= capacity / 6:
                sizes[0].append(weight)
            elif weight > capacity / 6 and weight <= capacity / 5:
                sizes[1].append(weight)
            elif weight > capacity / 5 and weight <= capacity / 4:
                sizes[2].append(weight)
            elif weight > capacity / 4 and weight <= capacity / 3:
                sizes[3].append(weight)
            elif weight > capacity / 3 and weight <= capacity / 2:
                sizes[4].append(weight)
            else:
                sizes[5].append(weight)
        return sizes
