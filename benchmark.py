import pyperf
from os import listdir
from os.path import isfile, join, basename
from macpacking.algorithms.online import NextFit as Nf_online, BestFit, WorstFit, TerriblePacker, FirstFit, RefinedFirstFit, FixedCapacityWF
from macpacking.algorithms.offline import NextFit as Nf_offline, FirstFitDecreasing, BestFitDecreasing, WorstFitDecreasing, RefinedFirstFitDecreasing, FixedCapacityBaseLine
from macpacking.algorithms.baseline import BenMaier
from macpacking.reader import BinppReader


class Benchmark:

    algos = {
        'terrible': TerriblePacker(),
        'nf-online': Nf_online(),
        'bf-online': BestFit(),
        'wf-online': WorstFit(),
        'ff-online': FirstFit(),
        'nf-offline': Nf_offline(),
        'bf-offline': BestFitDecreasing(),
        'wf-offline': WorstFitDecreasing(),
        'ff-offline': FirstFitDecreasing(),
        'baseline': BenMaier()
    }

    t4_algos = {
        'rff-online': RefinedFirstFit(),
        'rff-offline': RefinedFirstFitDecreasing()
    }

    t5_algos = {
        'fcwf': FixedCapacityWF,
        'fcbaseline': FixedCapacityBaseLine 
    }

    fixed_bins = 5
    
    CASES = './_datasets/binpp/N4C2W2'

    def __init__(self) -> None:
        self.algos
        self.t4_algos
        self.t5_algos
        self.fixed_bins
        self.CASES


    def list_case_files(self, dir: str) -> list[str]:
        return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir, f))])


    def run_bench(self, cases: list[str]):
        runner = pyperf.Runner()
        for case in cases:
            name = basename(case)
            data_online = BinppReader(case).online()
            data_offline = BinppReader(case).offline()
            for a in self.algos:
                if a == 'baseline' or a.endswith('offline'):
                    runner.bench_func(name + '-' + a, self.algos[a], data_offline)
                else:
                    runner.bench_func(name + '-' + a, self.algos[a], data_online)
    
    def run_t4_bench(self, cases: list[str]):
        runner = pyperf.Runner()
        for case in cases:
            name = basename(case)
            data_online = BinppReader(case).online()
            data_offline = BinppReader(case).offline()
            for a in self.t4_algos:
                if a == 'rff-online':
                    runner.bench_func(name + '-' + a, self.t4_algos[a], data_online)
                else:
                    runner.bench_func(name + '-' + a, self.t4_algos[a], data_offline)

    def run_t5(self, input):
        FixedCapacityWF()._process(input, self.fixed_bins)

    def run_t5baseline(self, input):
        FixedCapacityBaseLine()._process(input, self.fixed_bins)
    
    def run_t5_bench(self, cases: list[str]):
        runner = pyperf.Runner()
        for case in cases:
            name = basename(case)
            data_online = BinppReader(case).online()
            data_offline = BinppReader(case).offline()
            for a in self.t5_algos:
                if a == 'fcwf':
                    runner.bench_func(name + '-' + a, self.run_t5, data_online[1])
                else:
                    runner.bench_func(name + '-' + a, self.run_t5baseline, data_offline[1])


def main():
    '''Example of benchmark code'''
    benchmark = Benchmark()
    cases = benchmark.CASES
    cases = benchmark.list_case_files(cases)
    #benchmark.run_bench(cases)
    #benchmark.run_t4_bench(cases)
    benchmark.run_t5_bench(cases)

if __name__ == "__main__":
    main()
