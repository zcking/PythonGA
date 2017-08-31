import random
import datetime
import unittest
import random

import src.ch01.genetic as genetic


def get_fitness(guess, target):
    # Measure how fit the guess was
    return sum(1 for expected, actual in zip(target, guess) if expected == actual)


def display(candidate: genetic.Chromosome, start_time):
    time_diff = datetime.datetime.now() - start_time
    print('{genes}\t{fitness}\t{timing}'.format(
        genes=candidate.genes, fitness=candidate.fitness, timing=str(time_diff)
    ))


class GuessPasswordTests(unittest.TestCase):
    gene_set = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLNOPQRSTUVWXYZ!."

    def test_Hello_World(self):
        target = 'Hello World!'
        self.guess_password(target)

    def test_For_I_am_fearfully_and_wonderfully_made(self):
        target = 'For I am fearfully and wonderfully made.'
        self.guess_password(target)

    def test_benchmark(self):
        genetic.Benchmark.run(self.test_Random)

    def test_Random(self):
        length = 150
        target = ''.join(random.choice(self.gene_set) for _ in range(length))
        self.guess_password(target=target)

    def guess_password(self, target):
        start_time = datetime.datetime.now()

        def fn_get_fitness(genes):
            return get_fitness(guess=genes, target=target)

        def fn_display(candidate: genetic.Chromosome):
            display(candidate=candidate, start_time=start_time)

        optimal_fitness = len(target)
        best = genetic.get_best(
            get_fitness=fn_get_fitness,
            target_len=len(target), optimal_fitness=optimal_fitness,
            gene_set=self.gene_set, display=fn_display
        )
        self.assertEqual(best.genes, target)

if __name__ == '__main__':
    unittest.main()
