import os
import unittest
import datetime
import random

from src import guess_password
from src import genetic

class GuessPasswordTests(unittest.TestCase):
    gene_set = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLNOPQRSTUVWXYZ!."

    def test_Hello_World(self):
        target = 'Hello World!'
        self.guess_password(target)

    def test_For_I_am_fearfully_and_wonderfully_made(self):
        target = 'For I am fearfully and wonderfully made.'
        self.guess_password(target)

    @unittest.skipIf(os.environ.get('SKIP_BENCHMARK_TESTS', False), 'env variable set to skip benchmarks')
    def test_benchmark(self):
        genetic.Benchmark.run(self.test_Random, runs=5)

    def test_Random(self):
        length = 150
        target = ''.join(random.choice(self.gene_set) for _ in range(length))
        self.guess_password(target=target)

    def test_empty_string(self):
        target = ''
        self.guess_password(target)

    def guess_password(self, target):
        start_time = datetime.datetime.now()

        def fn_get_fitness(genes):
            return guess_password.get_fitness(guess=genes, target=target)

        def fn_display(candidate: genetic.Chromosome):
            guess_password.display(candidate=candidate, start_time=start_time)

        optimal_fitness = len(target)
        best = genetic.get_best(
            get_fitness=fn_get_fitness,
            target_len=len(target), optimal_fitness=optimal_fitness,
            gene_set=self.gene_set, display=fn_display
        )
        self.assertEqual(''.join(best.genes), target)

if __name__ == '__main__':
    unittest.main()
