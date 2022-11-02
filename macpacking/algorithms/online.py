from .. import Solution, WeightStream
from ..model import Online


class NextFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_index = 0
        solution = [[]]
        remaining = capacity
        for w in stream:
            if remaining >= w:
                solution[bin_index].append(w)
                remaining = remaining - w
            else:
                bin_index += 1
                solution.append([w])
                remaining = capacity - w
        return solution


class TerriblePacker(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = []
        for w in stream:
            solution.append([w])
        return solution


class FirstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [[]]
        remaining = capacity
        for w in stream:
            remaining -= w
            if remaining<0:
                solution.append([w])
                remaining = capacity - w
            else:
                solution[len(solution)-1].append(w)
        return solution      
        
        
class BestFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [[]]
        remaining = []
        for w in stream:
            assigned = False
            for room in range(len(remaining)):
                if remaining[room] + w <= capacity:
                    solution[room].append(w)
                    remaining[room] += w
                    assigned = True
                    break
            if not assigned:
                solution.append([w]) 
                remaining.append(w)
        return solution 


class WorstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        pass
