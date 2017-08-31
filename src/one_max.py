import datetime

from src import genetic

def get_fitness(genes):
    return genes.count(1)


def display(candidate: genetic.Chromosome, start_time):
    time_diff = datetime.datetime.now() - start_time
    print('{front:^15}...{back:^15} {fitness:^4.2f} {timing:^20}'.format(
        front=''.join(map(str, candidate.genes[:15])),
        back=''.join(map(str, candidate.genes[-15:])),
        fitness=candidate.fitness,
        timing=str(time_diff)
    ))