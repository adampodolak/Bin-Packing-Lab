from .. import Solution, WeightSet
from ..model import Offline, OfflineT5
from .online import NextFit as Nf_online
from .online import FirstFit as Ff_online
from .online import BestFit as Bf_online
from .online import WorstFit as Wf_online
from .online import RefinedFirstFit as RFF_online
import binpacking as bp


class NextFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of NextFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Nf_online()
        return delegation((capacity, weights))


class FirstFitDecreasing(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        weights = sorted(weights, reverse=True)
        delegation = Ff_online()
        return delegation((capacity, weights))


class BestFitDecreasing(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        weights = sorted(weights, reverse=True)
        delegation = Bf_online()
        return delegation((capacity, weights))


class WorstFitDecreasing(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        weights = sorted(weights, reverse=True)
        delegation = Wf_online()
        return delegation((capacity, weights))


class RefinedFirstFitDecreasing(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        weights = sorted(weights, reverse=True)
        delegation = RFF_online()
        return delegation((capacity, weights))


class FixedCapacityBaseLine(OfflineT5):

    def _process(self, weights: WeightSet, numOfBins: int) -> Solution:
        bins = bp.to_constant_bin_number(weights, numOfBins)
        return bins
