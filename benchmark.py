import pyperf
from os import listdir
from os.path import isfile, join, basename
from macpacking.algorithms.online import NextFit as Nf_online, BestFit, WorstFit, TerriblePacker, FirstFit, RefinedFirstFit
from macpacking.algorithms.offline import NextFit as Nf_offline, FirstFitDecreasing, BestFitDecreasing, WorstFitDecreasing, RefinedFirstFitDecreasing
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
    
    CASES = './_datasets/binpp/N4C2W2'

    def __init__(self) -> None:
        self.algos
        self.t4_algos
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

def main():
    '''Example of benchmark code'''
    benchmark = Benchmark()
    cases = benchmark.CASES
    cases = benchmark.list_case_files(cases)
    #benchmark.run_bench(cases)
    benchmark.run_t4_bench(cases)

if __name__ == "__main__":
    main()
