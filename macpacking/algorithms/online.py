from .. import Solution, WeightStream
from ..model import Online, OnlineT5
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

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
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
                if currcapacity[room] + w <= capacity and (
                        currcapacity[room] + w > bestsize):
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
            bestsize = capacity + 1
            bestindex = 0
            for room in range(len(solution)):
                if currcapacity[room] + w <= capacity and (
                        currcapacity[room] + w < bestsize):
                    bestindex = room
                    bestsize = currcapacity[room] + w

            if bestsize == capacity + 1:
                solution.append([w])
                currcapacity.append(w)
            else:
                solution[bestindex].append(w)
                currcapacity[bestindex] += w
        return solution


class RefinedFirstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        sizes = T4Reader.normalize(capacity, stream)
        solution = [[]]
        binCounter = 0
        maxFit = len(sizes) + 1
        for category in sizes:
            maxFit -= 1
            temp = maxFit
            for object in category:
                solution[binCounter].append(object)
                temp -= 1
                if temp == 0:
                    solution.append([])
                    binCounter += 1
                    temp = maxFit
            if solution[binCounter]:
                solution.append([])
                binCounter += 1
        if not solution[len(solution) - 1]:
            solution.pop()
        return solution


class FixedCapacityWF(OnlineT5):

    def _process(self, stream: WeightStream, numOfBins: int) -> Solution:
        solution = []
        currcapacity = []
        for i in range(numOfBins):
            solution.append([])
            currcapacity.append(0)
        for w in stream:
            bestsize = 1000  # arbitrary large num
            bestindex = 0
            for room in range(numOfBins):
                if currcapacity[room] + w < bestsize:
                    bestindex = room
                    bestsize = currcapacity[room] + w

            if bestsize != 1000:
                solution[bestindex].append(w)
                currcapacity[bestindex] += w
            else:
                if len(solution) <= numOfBins:
                    solution.append([w])
                    currcapacity.append(w)
                else:
                    return "cannot fit all objects into bins"
        return solution
