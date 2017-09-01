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
