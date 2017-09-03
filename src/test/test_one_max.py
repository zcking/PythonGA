import os
import unittest
import datetime

from src import genetic
from src import one_max

class OneMaxTests(unittest.TestCase):
    def test(self, length=100):
        gene_set = [0, 1]
        start_time = datetime.datetime.now()

        def fn_display(candidate):
            one_max.display(candidate, start_time)

        def fn_get_fitness(genes):
            return one_max.get_fitness(genes)

        optimal_fitness = length
        best = genetic.get_best(
            get_fitness=fn_get_fitness,
            target_len=length,
            optimal_fitness=optimal_fitness,
            gene_set=gene_set,
            display=fn_display
        )
        self.assertEqual(best.fitness, optimal_fitness)

    @unittest.skipIf(os.environ.get('SKIP_BENCHMARK_TESTS', False), 'env variable set to skip benchmarks')
    def test_benchmark(self):
        genetic.Benchmark.run(lambda: self.test(length=4000), runs=5)