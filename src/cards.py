import random
import datetime
import operator
import functools


class Fitness(object):
    group1_sum = None
    group2_product = None
    total_difference = None
    duplicate_count = None

    def __init__(self, group1_sum, group2_product, duplicate_count):
        self.group1_sum = group1_sum
        self.group2_product = group2_product
        sum_difference = abs(36 - group1_sum)
        product_difference = abs(360 - group2_product)
        self.total_difference = sum_difference + product_difference
        self.duplicate_count = duplicate_count

    def __gt__(self, other: 'Fitness'):
        if self.duplicate_count != other.duplicate_count:
            return self.duplicate_count < other.duplicate_count
        return self.total_difference < other.total_difference

    def __str__(self):
        return 'sum: {0} prod: {1} dups: {2}'.format(
            self.group1_sum,
            self.group2_product,
            self.duplicate_count
        )


def get_fitness(genes):
    group1_sum = sum(genes[0:5])
    group2_product = functools.reduce(operator.mul, genes[5:10])
    duplicate_count = len(genes) - len(set(genes))
    return Fitness(group1_sum, group2_product, duplicate_count)


def display(candidate, start_time):
    time_diff = datetime.datetime.now() - start_time
    print('{group1} - {group2}\t{fitness}\t{timing}'.format(
        group1=', '.join(map(str, candidate.genes[0:5])),
        group2=', '.join(map(str, candidate.genes[5:10])),
        fitness=candidate.fitness,
        timing=str(time_diff)
    ))


def mutate(genes, gene_set):
    # If there are no duplicates, swap the two genes
    # otherwise, mutate 1 random gene
    if len(genes) == len(set(genes)):
        # Swap two random genes n times where n is also random
        count = random.randint(1, 4)
        while count > 0:
            count -= 1
            index_a, index_b = random.sample(range(len(genes)), 2)
            genes[index_a], genes[index_b] = genes[index_b], genes[index_a]
    else:
        index_a = random.randrange(0, len(genes))
        index_b = random.randrange(0, len(gene_set))
        genes[index_a] = gene_set[index_b]
