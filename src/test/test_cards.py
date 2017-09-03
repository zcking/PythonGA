
import unittest
import datetime

from src import genetic
from src import cards


class CardTests(unittest.TestCase):
    def test(self, num_cards=10, group1_sum=36, group2_product=360):
        gene_set = [i + 1 for i in range(num_cards)]
        start_time = datetime.datetime.now()

        def fn_display(candidate):
            cards.display(candidate, start_time)

        def fn_get_fitness(genes):
            return cards.get_fitness(genes)

        def fn_mutate(genes):
            cards.mutate(genes, gene_set)

        optimal_fitness = cards.Fitness(
            group1_sum=group1_sum,
            group2_product=group2_product,
            duplicate_count=0
        )
        best = genetic.get_best(
            get_fitness=fn_get_fitness,
            target_len=num_cards,
            optimal_fitness=optimal_fitness,
            gene_set=gene_set,
            display=fn_display,
            custom_mutate=fn_mutate
        )
        self.assertTrue(not optimal_fitness > best.fitness)

    def test_fitness_greater_than_operator(self):
        fitness1 = cards.Fitness(0, 0, 0)
        fitness2 = cards.Fitness(0, 0, 1)
        self.assertTrue(fitness1 > fitness2)

        fitness1 = cards.Fitness(0, 0, 0)
        fitness2 = cards.Fitness(1, 1, 0)
        self.assertTrue(fitness2 > fitness1)
