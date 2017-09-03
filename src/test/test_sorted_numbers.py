import os
import unittest
import datetime

from src import genetic
from src import sorted_numbers


class SortedNumbersTests(unittest.TestCase):
    def test_sort_10_numbers(self):
        self.sort_numbers(10)

    def test_benchmark(self):
        runs = 5
        if os.environ.get('MINIMAL_BENCHMARK_TESTS', False):
            runs = 1
        genetic.Benchmark.run(lambda: self.sort_numbers(length=40), runs=runs)

    def sort_numbers(self, length=5):
        gene_set = [i for i in range(100)]
        start_time = datetime.datetime.now()

        def fn_display(candidate):
            sorted_numbers.display(candidate, start_time)

        def fn_get_fitness(genes):
            return sorted_numbers.get_fitness(genes)

        optimal_fitness = genetic.Fitness(length, 0)
        best = genetic.get_best(
            get_fitness=fn_get_fitness,
            target_len=length,
            optimal_fitness=optimal_fitness,
            gene_set=gene_set,
            display=fn_display
        )
        self.assertTrue(not optimal_fitness > best.fitness)