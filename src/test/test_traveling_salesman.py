import unittest
import os
import datetime

from src import genetic, traveling_salesman


class TSPTests(unittest.TestCase):
    def test_five_cities(self):
        city_a = traveling_salesman.Node('A')
        city_b = traveling_salesman.Node('B')
        city_c = traveling_salesman.Node('C')
        city_d = traveling_salesman.Node('D')
        city_e = traveling_salesman.Node('E')

        city_a.add_edge(city_b, 16)
        city_a.add_edge(city_e, 22)
        city_a.add_edge(city_d, 14)
        city_b.add_edge(city_e, 4)
        city_b.add_edge(city_c, 18)
        city_d.add_edge(city_c, 19)
        city_d.add_edge(city_e, 7)

        self.find_cheapest_route(nodes=[
            city_a, city_b, city_c,
            city_d, city_e
        ], optimal_cost=-43)

    def test_four_cities(self):
        city_a = traveling_salesman.Node('A')
        city_b = traveling_salesman.Node('B')
        city_c = traveling_salesman.Node('C')
        city_d = traveling_salesman.Node('D')

        city_a.add_edge(city_b, 3)
        city_a.add_edge(city_c, 5)
        city_a.add_edge(city_d, 2)
        city_b.add_edge(city_c, 4)
        city_b.add_edge(city_d, 6)
        city_c.add_edge(city_d, 2)

        nodes = [city_a, city_b, city_c, city_d]
        self.find_cheapest_route(nodes, optimal_cost=-7)

    def find_cheapest_route(self, nodes, optimal_cost):
        print('Defined Map:')
        for city in nodes:
            print('{0} -> {1}'.format(city, ', '.join(map(str, city.linked_cities))))
        print('')

        # Okay, now we have 5 cities, each connected to all the other cities with a random cost 1-10

        gene_set = nodes[:]
        start_time = datetime.datetime.now()

        def fn_display(candidate):
            traveling_salesman.display(candidate, start_time)

        def fn_get_fitness(genes):
            return traveling_salesman.get_fitness(genes, gene_set)

        def fn_mutate(genes):
            traveling_salesman.mutate(genes, gene_set)

        best = genetic.get_best(
            get_fitness=fn_get_fitness,
            target_len=len(gene_set),
            optimal_fitness=optimal_cost,
            gene_set=gene_set,
            display=fn_display,
            custom_mutate=fn_mutate
        )
        self.assertTrue(not optimal_cost > best.fitness)

    def test_benchmark(self):
        runs = 100
        if os.environ.get('MINIMAL_BENCHMARK_TESTS', False):
            runs = 1
        genetic.Benchmark.run(lambda: self.test_five_cities(), runs=runs)

    def test_create_node(self):
        city_a = traveling_salesman.Node('A')
        city_b = traveling_salesman.Node('B', linked_cities={city_a: 4})
        self.assertEqual(city_a.value, 'A')
        self.assertEqual(city_b.linked_cities[city_a], 4)

    def test_node_eq_and_ne(self):
        city_a = traveling_salesman.Node('A')
        city_a_2 = traveling_salesman.Node('A')
        city_b = traveling_salesman.Node('B')
        self.assertEqual(city_a, city_a_2)
        self.assertNotEqual(city_a, city_b)

    def test_repr(self):
        city_a = traveling_salesman.Node('A')
        self.assertEqual(repr(city_a), str(city_a))

    def test_get_fitness(self):
        city_a = traveling_salesman.Node('A')
        city_b = traveling_salesman.Node('B')
        city_a.add_edge(city_b, 5)

        # Test it without duplicates
        best_fitness = traveling_salesman.get_fitness([city_a, city_b], [city_a, city_b])
        self.assertEqual(best_fitness, -5)

        # Test it with duplicates
        bad_fitness = traveling_salesman.get_fitness([city_a, city_a], [city_a, city_b])
        self.assertTrue(bad_fitness < best_fitness)

        print('Fitness w/o duplicates: {0}\nFitness w/ duplicates: {1}'.format(
            best_fitness, bad_fitness
        ))

    def test_mutation_without_duplicates(self):
        city_a = traveling_salesman.Node('A')
        city_b = traveling_salesman.Node('B')
        city_a.add_edge(city_b, 5)
        genes = [city_a, city_b] # A -> B
        original_genes = genes[:]
        gene_set = [city_a, city_b]

        traveling_salesman.mutate(genes, gene_set)
        self.assertCountEqual(original_genes, genes)

    def test_mutation_with_duplicates(self):
        city_a = traveling_salesman.Node('A')
        city_b = traveling_salesman.Node('B')
        city_a.add_edge(city_b, 5)
        genes = [city_a, city_a]
        original_genes = genes[:]
        gene_set = [city_a, city_b]

        traveling_salesman.mutate(genes, gene_set)
        self.assertCountEqual(original_genes, genes)
