import pyperf
from os import listdir
from os.path import isfile, join, basename
from macpacking.algorithms.online import NextFit
from macpacking.reader import BinppReader
from macpacking.algorithms.online import FirstFit, BestFit




CASES = './_datasets/binpp/N4C2W2'


def main():
    '''Example of benchmark code'''
    cases = list_case_files(CASES)

    run_bench([NextFit(), FirstFit()], cases)

def list_case_files(dir: str) -> list[str]:
    return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir, f))])


def run_bench(algo, cases: list[str]):
    runner = pyperf.Runner()
    for case in cases[0:1]:
        name = basename(case)
        data = BinppReader(case).online()
        for a in range(len(algo)):
            runner.bench_func(name+ str(a), algo[a], data)


if __name__ == "__main__":
    main()
