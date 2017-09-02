import unittest
import datetime

from src import genetic
from src import eight_queens


class EightQueensTest(unittest.TestCase):
    def test(self, size=8):
        gene_set = [i for i in range(size)]
        start_time = datetime.datetime.now()

        def fn_display(candidate):
            eight_queens.display(candidate, start_time, size)

        def fn_get_fitness(genes):
            return eight_queens.get_fitness(genes, size)

        optimal_fitness = eight_queens.Fitness(0)
        best = genetic.get_best(
            get_fitness=fn_get_fitness,
            target_len=size * 2,
            optimal_fitness=optimal_fitness,
            gene_set=gene_set,
            display=fn_display
        )
        self.assertTrue(not optimal_fitness > best.fitness)

    def test_benchmark(self):
        genetic.Benchmark.run(lambda: self.test(size=20), runs=5)
