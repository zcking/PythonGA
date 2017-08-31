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
    genes = ''.join(genes)
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)


def _mutate(parent, gene_set, get_fitness):
    # Mutate one of the genes of the parent randomly
    index = random.randrange(0, len(parent.genes))
    child_genes = list(parent.genes)
    new_gene, alternate = random.sample(gene_set, 2)
    child_genes[index] = alternate \
        if new_gene == child_genes[index] \
        else new_gene
    genes = ''.join(child_genes)
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)


def get_best(get_fitness, target_len, optimal_fitness, gene_set, display):
    random.seed()
    best_parent = _generate_parent(length=target_len, gene_set=gene_set, get_fitness=get_fitness)
    display(best_parent)
    if best_parent.fitness >= optimal_fitness:
        return best_parent

    while True:
        child = _mutate(parent=best_parent, gene_set=gene_set, get_fitness=get_fitness)

        if best_parent.fitness >= child.fitness:
            continue

        display(child)

        if child.fitness >= optimal_fitness:
            return child

        best_parent = child


class Chromosome(object):
    genes = None
    fitness = None

    def __init__(self, genes, fitness):
        self.genes = genes
        self.fitness = fitness


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
