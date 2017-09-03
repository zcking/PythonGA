import os
import unittest
import datetime

from src import genetic, states_coloring


class StatesColoringTests(unittest.TestCase):
    def test(self):
        states = states_coloring.load_data(file_name='adjacent_states.csv')
        rules = states_coloring.build_rules(states)
        optimal_value = len(rules)
        state_index_lookup = {key: index for index, key in enumerate(sorted(states))}

        colors = ['Orange', 'Yellow', 'Blue', 'Green']
        color_lookup = {color[0]: color for color in colors}
        gene_set = list(color_lookup.keys()) # ['O', 'Y', 'B', 'G']

        start_time = datetime.datetime.now()

        def fn_display(candidate):
            states_coloring.display(candidate, start_time)

        def fn_get_fitness(genes):
            return states_coloring.get_fitness(genes, rules, state_index_lookup)

        best = genetic.get_best(
            get_fitness=fn_get_fitness,
            target_len=len(states),
            optimal_fitness=optimal_value,
            gene_set=gene_set,
            display=fn_display
        )
        self.assertTrue(not optimal_value > best.fitness)

        keys = sorted(states.keys())
        for index in range(len(states)):
            print(keys[index] + ' is ' + color_lookup[best.genes[index]])

    def test_benchmark(self):
        runs = 10
        if os.environ.get('MINIMAL_BENCHMARK_TESTS', False):
            runs = 1
        genetic.Benchmark.run(lambda: self.test(), runs=runs)
