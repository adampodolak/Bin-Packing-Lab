from macpacking.reader import DatasetReader, BinppReader, JBurkardtReader
import pytest


def test_binpp_reader():
    dataset = '_datasets/binpp/N1C1W1/N1C1W1_B.BPP.txt'
    capacity = 100
    oracle = [
        8, 8, 12, 13, 13, 14, 15, 17, 18, 19, 20, 23, 30, 37, 37, 39, 40,
        43, 43, 44, 44, 50, 51, 61, 61, 62, 62, 63, 66, 67, 69, 70, 71,
        72, 75, 76, 76, 79, 83, 83, 88, 92, 92, 93, 93, 97, 97, 97, 99, 100
    ]
    reader: DatasetReader = BinppReader(dataset)
    assert capacity == reader.offline()[0]
    assert oracle == sorted(reader.offline()[1])


def test_jburkardt_reader():
    capacity_input = '_datasets/jburkardt/p01_c.txt'
    weights_input = '_datasets/jburkardt/p01_w.txt'
    capacity = 100
    weights = [3, 7, 11, 33, 33, 33, 50, 60, 70]
    reader: DatasetReader = JBurkardtReader(capacity_input, weights_input)
    assert capacity == reader.offline()[0]
    assert weights == sorted(reader.offline()[1])
