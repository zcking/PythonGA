import random
import time
import sys
import statistics

def _generate_parent(length, gene_set, get_fitness):
    # Generate a parent with random sampling of genes from gene set
    genes = []
    while len(genes) < length:
        sample_size = min(length - len(genes), len(gene_set))
        genes.extend(random.sample(gene_set, sample_size))
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)


def _mutate(parent, gene_set, get_fitness):
    # Mutate one of the genes of the parent randomly
    index = random.randrange(0, len(parent.genes))
    child_genes = parent.genes[:]
    new_gene, alternate = random.sample(gene_set, 2)
    child_genes[index] = alternate \
        if new_gene == child_genes[index] \
        else new_gene
    fitness = get_fitness(child_genes)
    return Chromosome(child_genes, fitness)


def _get_improvement(new_child, generate_parent):
    best_parent = generate_parent()
    yield best_parent

    while True:
        child = new_child(best_parent)
        if best_parent.fitness > child.fitness:
            continue

        if not child.fitness > best_parent.fitness:
            best_parent = child
            continue

        yield child
        best_parent = child


def get_best(get_fitness, target_len, optimal_fitness, gene_set, display):
    random.seed()

    def fn_mutate(parent):
        return _mutate(parent=parent, gene_set=gene_set, get_fitness=get_fitness)

    def fn_generate_parent():
        return _generate_parent(target_len, gene_set, get_fitness)

    for improvement in _get_improvement(fn_mutate, fn_generate_parent):
        display(improvement)

        # Found optimal fitness?
        if not optimal_fitness > improvement.fitness:
            return improvement


class Chromosome(object):
    genes = None
    fitness = None

    def __init__(self, genes, fitness):
        self.genes = genes
        self.fitness = fitness


class Fitness(object):
    numbers_in_sequence_count = None
    total_gap = None

    def __init__(self, numbers_in_sequence_count, total_gap):
        self.numbers_in_sequence_count = numbers_in_sequence_count
        self.total_gap = total_gap


    def __gt__(self, other: 'Fitness'):
        if self.numbers_in_sequence_count != other.numbers_in_sequence_count:
            return self.numbers_in_sequence_count > other.numbers_in_sequence_count
        return self.total_gap < other.total_gap

    def __str__(self):
        return '{seq} Sequential, {gap} Total Gap'.format(
            seq=self.numbers_in_sequence_count,
            gap=self.total_gap
        )


class Benchmark(object):
    @staticmethod
    def run(function, runs=10):
        timings = []
        print('{0:^10} {1:^10} {2:^10}'.format(
            'Run Index', 'Mean', 'Std Dev'
        ))
        stdout = sys.stdout
        for i in range(runs):
            sys.stdout = None
            start_time = time.time()
            function()
            seconds = time.time() - start_time
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i < 10 or i % 10 == 9:
                print('{run_index:^10} {mean:^10.2f} {stdev:^10.2f}'.format(
                    run_index=i + 1, mean=mean,
                    stdev=statistics.stdev(timings, mean)
                    if i > 1 else 0
                ))
