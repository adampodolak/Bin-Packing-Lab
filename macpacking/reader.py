from abc import ABC, abstractmethod
from os import path
from random import shuffle, seed
from . import WeightSet, WeightStream


class DatasetReader(ABC):

    def offline(self) -> WeightSet:
        '''Return a WeightSet to support an offline algorithm'''
        (capacity, weights) = self._load_data_from_disk()
        seed(42)          # always produce the same shuffled result
        shuffle(weights)  # side effect shuffling
        return (capacity, weights)

    def online(self) -> WeightStream:
        '''Return a WeighStream, to support an online algorithm'''
        (capacity, weights) = self.offline()

        def iterator():  # Wrapping the contents into an iterator
            for w in weights:
                yield w  # yields the current value and moves to the next one

        return (capacity, iterator())

    @abstractmethod
    def _load_data_from_disk(self) -> WeightSet:
        '''Method that read the data from disk, depending on the file format'''
        pass


class BinppReader(DatasetReader):
    '''Read problem description according to the BinPP format'''

    def __init__(self, filename: str) -> None:
        if not path.exists(filename):
            raise ValueError(f'Unkown file [{filename}]')
        self.__filename = filename

    def _load_data_from_disk(self) -> WeightSet:
        with open(self.__filename, 'r') as reader:
            nb_objects: int = int(reader.readline())
            capacity: int = int(reader.readline())
            weights = []
            for _ in range(nb_objects):
                weights.append(int(reader.readline()))
            return (capacity, weights)

class JBurkardtReader(DatasetReader):
    
    def __init__(self, capacity_file: str, weights_file: str) -> None:
        if not path.exists(capacity_file):
            raise ValueError(f'Unkown file [{capacity_file}]')
        elif not path.exists(weights_file):
            raise ValueError(f'unknown file [{weights_file}]')
        self.__filename = capacity_file, weights_file
    
    def _load_data_from_disk(self) -> WeightSet:
        cfile, wfile = self.__filename
        with open(cfile, 'r') as capacity_reader, open(wfile, 'r') as w_reader:
            capacity: int = int(capacity_reader.readline())
            weights: list[int] = []
            while True:
                hold = w_reader.readline().strip('\n').strip()
                if not hold:
                    break
                else:
                    weights.append(int(hold))
            return (capacity, weights)

