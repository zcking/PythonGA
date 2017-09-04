
import datetime
import random

from src import genetic


class Node(object):
    def __init__(self, value, linked_cities=None):
        self.value = value
        if linked_cities is None:
            self.linked_cities = dict()
        else:
            self.linked_cities = linked_cities

    def add_edge(self, other_node, cost):
        if other_node in self.linked_cities:
            return
        self.linked_cities[other_node] = cost
        other_node.add_edge(self, cost)

    def __ne__(self, other):
        return self.value != other.value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.value)


def get_cost(genes):
    prev_node = genes[0]
    total_cost = 0

    for node in genes[1:]:
        total_cost += prev_node.linked_cities.get(node, 1000)
        prev_node = node

    return total_cost


def get_fitness(genes, gene_set):
    fitness = -1 * get_cost(genes)  # we use a different scale where 0 is the max and poorer fitnesses are < 0
    num_duplicates = len(genes) - len(set(genes))
    if num_duplicates > 0:
        fitness -= num_duplicates * 1000
    fitness -= (len(gene_set) - len(set(genes))) * 1000 # also subtract number of missing
    return fitness


def display(candidate: genetic.Chromosome, start_time):
    time_diff = datetime.datetime.now() - start_time
    print('{genes}\t\t{fitness}\t\t{timing}'.format(
        genes=' -> '.join(map(str, candidate.genes)),
        fitness=abs(candidate.fitness),
        timing=str(time_diff)
    ))


def mutate(genes, gene_set, shuffle_chance=0.1):
    if len(genes) == len(set(genes)):
        mut_index_1 = random.randrange(0, len(genes))
        mut_index_2 = random.randrange(0, len(genes))
        genes[mut_index_1], genes[mut_index_2] = genes[mut_index_2], genes[mut_index_1]
    else:
        count = random.randint(1, 4)
        for i in range(count):
            genes[random.randrange(0, len(genes))] = random.choice(gene_set)

    if random.random() <= shuffle_chance:
        random.shuffle(genes)

