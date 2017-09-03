import random
import datetime

from src import genetic


def get_fitness(guess, target):
    # Measure how fit the guess was
    return sum(1 for expected, actual in zip(target, guess) if expected == actual)


def display(candidate: genetic.Chromosome, start_time):
    time_diff = datetime.datetime.now() - start_time
    print('{genes}\t{fitness}\t{timing}'.format(
        genes=''.join(candidate.genes), fitness=candidate.fitness, timing=str(time_diff)
    ))


def mutate(genes, gene_set, target, index_to_known):
    initial_fitness = get_fitness(guess=genes, target=target)
    mutation_index = random.randrange(0, len(genes))
    new_gene, alternate = random.sample(gene_set, 2)
    new_genes = genes[:]
    new_genes[mutation_index] = alternate if new_gene == genes[mutation_index] else new_gene
    new_fitness = get_fitness(guess=new_genes, target=target)
    if not new_fitness > initial_fitness:
        index_to_known[mutation_index] = genes[mutation_index]
        return genetic.Chromosome(genes=genes, fitness=initial_fitness)
    else:
        if mutation_index in index_to_known and index_to_known[mutation_index] != new_gene:
            index_to_known[mutation_index] = new_gene
        genes[:] = new_genes
        return genetic.Chromosome(genes=new_genes, fitness=new_fitness)
