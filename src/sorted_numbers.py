import datetime

from src import genetic


def get_fitness(genes):
    fitness = 1
    gap = 0
    for i in range(1, len(genes)):
        if genes[i] > genes[i - 1]:
            fitness += 1
        else:
            gap += genes[i - 1] - genes[i]

    return genetic.Fitness(fitness, gap)


def display(candidate: genetic.Chromosome, start_time):
    time_diff = datetime.datetime.now() - start_time
    print('{genes:^20}\t=> {fitness}\t{timing:^10}'.format(
        genes=', '.join(map(str, candidate.genes)),
        fitness=candidate.fitness,
        timing=str(time_diff)
    ))
