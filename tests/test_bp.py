from unittest import result
from macpacking.algorithms.baseline import BenMaier
from macpacking.algorithms.online import BestFit, FirstFit, TerriblePacker, WorstFit
from macpacking.model import Offline, Online
from macpacking.reader import BinppReader, DatasetReader, JBurkardtReader

def test_baseline():
    dataset = '_datasets/binpp/N1C1W1/N1C1W1_B.BPP.txt'
    result = [[100], [99], [97], [97], [97], [93], [93],
        [92, 8], [92, 8], [88, 12], [83, 17], [83, 15], [79, 20],
            [76, 23], [76, 19], [75, 18], [72, 13, 13], [71], [70, 30],
                [69], [67], [66], [63, 37], [62, 37], [62], [61, 39], [61], 
                    [51, 44], [50, 44], [43, 43, 14], [40]]
    reader: DatasetReader = BinppReader(dataset)
    capacity = reader.offline()[0]
    weights = reader.offline()[1]
    packer: Offline = BenMaier()
    packer_result = packer._process(capacity, weights)
    assert result == packer_result

def test_terrible():
    weights_input =  '_datasets/jburkardt/p01_w.txt'
    capacity_input = '_datasets\jburkardt\p01_c.txt'
    result = [[33], [11], [7], [33], [3], [50], [33], [70], [60]]
    reader: DatasetReader = JBurkardtReader(capacity_input, weights_input)
    stream = reader.online()[1]
    packer: Online = TerriblePacker()
    packer_result = packer._process(stream)
    assert result == packer_result

def test_ffonline():
    weights_input =  '_datasets/jburkardt/p01_w.txt'
    capacity_input = '_datasets\jburkardt\p01_c.txt'
    result = [[33, 11, 7, 33, 3], [50, 33], [70], [60]]
    reader: DatasetReader = JBurkardtReader(capacity_input, weights_input)
    capacity = reader.online()[0]
    stream = reader.online()[1]
    packer: Online = FirstFit()
    packer_result = packer._process(capacity, stream)
    assert result == packer_result


def test_bfonline():
    weights_input =  '_datasets/jburkardt/p01_w.txt'
    capacity_input = '_datasets/jburkardt/p01_c.txt'
    result = [[11, 7, 33, 3], [33, 33], [50], [70], [60]]
    reader: DatasetReader = JBurkardtReader(capacity_input, weights_input)
    capacity = reader.online()[0]
    stream = reader.online()[1]
    packer: Online = BestFit()
    packer_result = packer._process(capacity, stream)
    #assert result == packer_result
    return packer_result

def test_wfonline():
    weights_input =  '_datasets/jburkardt/p01_w.txt'
    capacity_input = '_datasets/jburkardt/p01_c.txt'
    result = [[11, 7, 33, 3], [33, 33], [50], [70], [60]]
    reader: DatasetReader = JBurkardtReader(capacity_input, weights_input)
    capacity = reader.online()[0]
    stream = reader.online()[1]
    packer: Online = WorstFit()
    packer_result = packer._process(capacity, stream)
    #assert result == packer_result
    return packer_result


print(test_bfonline())
print(test_wfonline())