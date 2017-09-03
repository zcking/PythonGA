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

    def test_Hello_World_with_custom_mutation(self):
        target = 'Hello World'
        self.guess_password(target, use_custom_mutator=True)

    def test_For_I_am_fearfully_and_wonderfully_made(self):
        target = 'For I am fearfully and wonderfully made.'
        self.guess_password(target)

    def test_benchmark(self):
        runs = 5
        if os.environ.get('MINIMAL_BENCHMARK_TESTS', False):
            runs = 1
        genetic.Benchmark.run(self.test_Random, runs=runs)

    def test_benchmark_with_custom_mutator(self):
        runs = 5
        if os.environ.get('MINIMAL_BENCHMARK_TESTS', False):
            runs = 1
        genetic.Benchmark.run(self.test_Random_with_custom_mutator, runs=runs)

    def test_Random(self, use_custom_muator=False):
        length = 150
        target = ''.join(random.choice(self.gene_set) for _ in range(length))
        self.guess_password(target=target, use_custom_mutator=use_custom_muator)

    def test_Random_with_custom_mutator(self):
        self.test_Random(use_custom_muator=True)

    def test_empty_string(self):
        target = ''
        self.guess_password(target)

    def guess_password(self, target, use_custom_mutator=False):
        start_time = datetime.datetime.now()
        index_to_known = dict()

        def fn_get_fitness(genes):
            return guess_password.get_fitness(guess=genes, target=target)

        def fn_display(candidate: genetic.Chromosome):
            guess_password.display(candidate=candidate, start_time=start_time)

        def fn_mutate(genes):
            guess_password.mutate(
                genes=genes,
                gene_set=self.gene_set,
                target=target,
                index_to_known=index_to_known
            )

        optimal_fitness = len(target)
        if use_custom_mutator:
            best = genetic.get_best(
                get_fitness=fn_get_fitness,
                target_len=len(target), optimal_fitness=optimal_fitness,
                gene_set=self.gene_set, display=fn_display,
                custom_mutate=fn_mutate
            )
        else:
            best = genetic.get_best(
                get_fitness=fn_get_fitness,
                target_len=len(target), optimal_fitness=optimal_fitness,
                gene_set=self.gene_set, display=fn_display
            )
        self.assertEqual(''.join(best.genes), target)
