from macpacking.algorithms.baseline import BenMaier
from macpacking.algorithms.online import (
    BestFit, FirstFit, TerriblePacker, WorstFit,
    RefinedFirstFit, FixedCapacityWF)
from macpacking.algorithms.offline import FixedCapacityBaseLine
from macpacking.model import Offline, Online, OnlineT5, OfflineT5
from macpacking.reader import BinppReader, DatasetReader, JBurkardtReader
import pytest


def test_baseline():
    dataset = '_datasets/binpp/N1C1W1/N1C1W1_B.BPP.txt'
    result = [
        [100], [99], [97], [97], [97], [93], [93],
        [92, 8], [92, 8], [88, 12], [83, 17], [83, 15], [79, 20],
        [76, 23], [76, 19], [75, 18], [72, 13, 13], [71], [70, 30],
        [69], [67], [66], [63, 37], [62, 37], [62], [61, 39], [61],
        [51, 44], [50, 44], [43, 43, 14], [40]
        ]
    reader: DatasetReader = BinppReader(dataset)
    capacity = reader.offline()[0]
    weights = reader.offline()[1]
    packer: Offline = BenMaier()
    packer_result = packer._process(capacity, weights)
    assert result == packer_result


def test_terrible():
    weights_input = '_datasets/jburkardt/p01_w.txt'
    capacity_input = '_datasets/jburkardt/p01_c.txt'
    result = [[33], [11], [7], [33], [3], [50], [33], [70], [60]]
    reader: DatasetReader = JBurkardtReader(capacity_input, weights_input)
    stream = reader.online()[1]
    packer: Online = TerriblePacker()
    packer_result = packer._process(0, stream)
    assert result == packer_result


def test_bfonline():
    weights_input = '_datasets/jburkardt/p02_w.txt'
    capacity_input = '_datasets/jburkardt/p02_c.txt'
    result = [
        [32, 6, 37, 3, 7], [43, 46], [79, 19],
        [64, 18], [50], [99], [94]]
    reader: DatasetReader = JBurkardtReader(capacity_input, weights_input)
    capacity = reader.online()[0]
    stream = reader.online()[1]
    packer: Online = BestFit()
    packer_result = packer._process(capacity, stream)
    assert result == packer_result


def test_wfonline():
    weights_input = '_datasets/jburkardt/p02_w.txt'
    capacity_input = '_datasets/jburkardt/p02_c.txt'
    result = [
        [32, 6, 37, 19], [43, 3, 7, 46], [79], [64],
        [50, 18], [99], [94]]
    reader: DatasetReader = JBurkardtReader(capacity_input, weights_input)
    capacity = reader.online()[0]
    stream = reader.online()[1]
    packer: Online = WorstFit()
    packer_result = packer._process(capacity, stream)
    assert result == packer_result


def test_RFFonline():
    weights_input = '_datasets/jburkardt/p02_w.txt'
    capacity_input = '_datasets/jburkardt/p02_c.txt'
    result = [
        [6, 3, 7], [19, 18], [32], [37, 43],
        [46, 50], [79], [64], [99], [94]]
    reader: DatasetReader = JBurkardtReader(capacity_input, weights_input)
    capacity = reader.offline()[0]
    stream = reader.offline()[1]
    packer: Offline = RefinedFirstFit()
    packer_result = packer._process(capacity, stream)
    assert result == packer_result


def test_ffonline():
    dataset = '_datasets/binpp/N1C1W1/N1C1W1_B.BPP.txt'
    result = [
        [13, 20], [61, 23, 15], [62, 8, 18], [69, 17],
        [83], [97, 37], [61, 8], [88, 43, 13], [44, 14, 12],
        [72, 30], [66, 19], [79], [97], [83, 37], [62],
        [100], [70, 44], [40, 43], [50], [67], [63], [76],
        [97, 39], [51], [93], [93], [92], [76], [75],
        [71], [99], [92]
        ]
    reader: DatasetReader = BinppReader(dataset)
    capacity = reader.online()[0]
    stream = reader.online()[1]
    packer: Online = FirstFit()
    packer_result = packer._process(capacity, stream)
    assert packer_result == result


def test_FixedCapacityWF_online():
    dataset = '_datasets/binpp/N1C1W1/N1C1W1_B.BPP.txt'
    result = [
        [61, 13, 44, 66, 37, 15, 70, 13, 43, 51, 92, 92],
        [62, 61, 79, 100, 63, 93, 71],
        [69, 88, 23, 62, 8, 18, 50, 37, 97, 75],
        [83, 72, 20, 83, 44, 17, 14, 76, 93, 99],
        [97, 43, 97, 40, 67, 8, 12, 30, 39, 76, 19]
        ]
    reader: DatasetReader = BinppReader(dataset)
    stream = reader.online()[1]
    packer: OnlineT5 = FixedCapacityWF()
    packer_result = packer._process(stream, 5)
    assert packer_result == result


def test_FixedCapacityBaseLine_Offline():
    dataset = '_datasets/binpp/N1C1W1/N1C1W1_B.BPP.txt'
    result = [
        [100, 88, 83, 70, 63, 51, 43, 37, 14, 8],
        [99, 92, 76, 72, 67, 50, 43, 30, 17, 12],
        [97, 93, 79, 71, 66, 44, 44, 37, 15, 8],
        [97, 93, 76, 75, 62, 61, 40, 20, 19, 13],
        [97, 92, 83, 69, 62, 61, 39, 23, 18, 13]
        ]
    reader: DatasetReader = BinppReader(dataset)
    stream = reader.offline()[1]
    packer: OfflineT5 = FixedCapacityBaseLine()
    packer_result = packer._process(stream, 5)
    assert packer_result == result
