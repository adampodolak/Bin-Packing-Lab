from .. import Solution, WeightStream
from ..model import Online
from ..T4Reader import T4Reader


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


class WorstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = []
        currcapacity = []
        for w in stream:
            bestsize = capacity +1
            bestindex = 0
            for room in range(len(solution)):
                if currcapacity[room] + w <= capacity and currcapacity[room] + w < bestsize:
                    bestindex = room
                    bestsize = currcapacity[room] + w

            if bestsize ==capacity +1:
                solution.append([w]) 
                currcapacity.append(w)  
            else:
                solution[bestindex].append(w)
                currcapacity[bestindex] += w 
        return solution

class RefinedFirstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        sizes = T4Reader.normalize(capacity, stream)
        print (sizes)
        solution = [[]]
        binCounter = 0
        maxFit = len(sizes) +1
        for category in sizes:
            maxFit -=1
            temp = maxFit
            for object in category:
                solution[binCounter].append(object)
                temp -=1
                if temp == 0:
                    solution.append([])
                    binCounter +=1
                    temp = maxFit
            if solution[binCounter]:
                solution.append([])
                binCounter+=1
        if not solution[len(solution)-1]:
            solution.pop()
        return solution
            
