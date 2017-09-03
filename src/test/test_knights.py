import os
import random
import unittest
import datetime

from src import genetic
from src import knights


class KnightsTests(unittest.TestCase):
    def test_3x4(self):
        width = 4
        height = 3
        self.find_knight_positions(width, height, 6)

    def test_8x8(self):
        width = height = 8
        self.find_knight_positions(width, height, 14)

    def test_10x10(self):
        width = height = 10
        self.find_knight_positions(width, height, 22)

    def test_benchmark(self):
        runs = 5
        if os.environ.get('MINIMAL_BENCHMARK_TESTS', False):
            runs = 1
        genetic.Benchmark.run(lambda: self.test_10x10(), runs=runs)

    def find_knight_positions(self, board_width, board_height, expected_knights):
        start_time = datetime.datetime.now()

        all_positions = [knights.Position(x, y)
                         for y in range(board_height)
                         for x in range(board_width)]

        if board_width < 6 or board_height < 6:
            non_edge_positions = all_positions
        else:
            non_edge_positions = [i for i in all_positions
                                  if 0 < i.x < board_width - 1 and
                                  0 < i.y < board_height - 1]

        def fn_display(candidate):
            knights.display(candidate, start_time, board_width, board_height)

        def fn_get_fitness(genes):
            return knights.get_fitness(genes, board_width, board_height)

        def fn_get_random_position():
            return random.choice(non_edge_positions)

        def fn_mutate(genes):
            knights.mutate(genes, board_width, board_height, all_positions, non_edge_positions)

        def fn_create():
            return knights.create(fn_get_random_position, expected_knights)

        # Optimal = entire board covered
        optimal_fitness = board_width * board_height
        best = genetic.get_best(
            get_fitness=fn_get_fitness,
            target_len=None,
            optimal_fitness=optimal_fitness,
            gene_set=None,
            display=fn_display,
            custom_mutate=fn_mutate,
            custom_create=fn_create
        )
        self.assertTrue(not optimal_fitness > best.fitness)
