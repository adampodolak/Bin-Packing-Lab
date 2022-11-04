from .. import Solution, WeightStream
from ..model import Online


class NextFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_index = 0
        solution = [[]]
        currcapacity = capacity
        for w in stream:
            if currcapacity >= w:
                solution[bin_index].append(w)
                currcapacity = currcapacity - w
            else:
                bin_index += 1
                solution.append([w])
                currcapacity = capacity - w
        return solution


class TerriblePacker(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = []
        for w in stream:
            solution.append([w])
        return solution


class FirstFit(Online):

    def _process(self, capacity:int, stream: WeightStream) -> Solution:
        solution = [[]]
        currcapacity = []
        for w in stream:
            assigned = False
            for room in range(len(currcapacity)):
                if currcapacity[room] + w <= capacity:
                    solution[room].append(w)
                    currcapacity[room] += w
                    assigned = True
                    break
            if not assigned:
                solution.append([w]) 
                currcapacity.append(w)   
        return solution
<<<<<<< HEAD
        
=======
>>>>>>> 45d47dc16f0a0ac68e9c223029f6ae2f5cdfa7e5

class BestFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = []
        currcapacity = []
        for w in stream:
            bestsize = 0
            bestindex = 0
            for room in range(len(solution)):
                print(currcapacity[room], w)
                if currcapacity[room] + w <= capacity and currcapacity[room] + w > bestsize:
                    bestindex = room
                    bestsize = currcapacity[room] + w

            if bestsize == 0:
                solution.append([w]) 
                currcapacity.append(w)  
            else:
                solution[bestindex].append(w)
                currcapacity[bestindex] += w
        return solution
<<<<<<< HEAD

=======
>>>>>>> 45d47dc16f0a0ac68e9c223029f6ae2f5cdfa7e5

class WorstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = []
        currcapacity = []
        for w in stream:
<<<<<<< HEAD
            bestsize = capacity +1
=======
            bestsize = capacity
>>>>>>> 45d47dc16f0a0ac68e9c223029f6ae2f5cdfa7e5
            bestindex = 0
            for room in range(len(solution)):
                if currcapacity[room] + w <= capacity and currcapacity[room] + w < bestsize:
                    bestindex = room
                    bestsize = currcapacity[room] + w

<<<<<<< HEAD
            if bestsize ==capacity +1:
=======
            if bestsize == 100:
>>>>>>> 45d47dc16f0a0ac68e9c223029f6ae2f5cdfa7e5
                solution.append([w]) 
                currcapacity.append(w)  
            else:
                solution[bestindex].append(w)
                currcapacity[bestindex] += w 
<<<<<<< HEAD


        return solution
            
=======
        return solution
>>>>>>> 45d47dc16f0a0ac68e9c223029f6ae2f5cdfa7e5
