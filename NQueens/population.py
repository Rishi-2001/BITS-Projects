import random
from chromosome import Chromosome


class Population:
    def __init__(self, k=20, nqueens=8, chromosomes=None):

        if chromosomes is None:
            self.nqueens = nqueens
            self.k = k
            row = random.randint(1, self.nqueens)
            queens = [row] * self.nqueens
            self.chromosomes = [Chromosome(genes=queens) for _ in range(k)]
        else:
            self.k = len(chromosomes)
            self.nqueens = chromosomes[0].length
            self.chromosomes = chromosomes

        self.probabilities = [
            chromosome.probability() for chromosome in self.chromosomes
        ]

    def pick(self, mode="wheel", tournament_size=2):
        if mode == "wheel":
            populationWithProbabilty = zip(self.chromosomes, self.probabilities)
            total = sum(w for c, w in populationWithProbabilty)
            r = random.uniform(0, total)
            upto = 0
            for c, w in zip(self.chromosomes, self.probabilities):
                if upto + w >= r:
                    return c
                upto += w
            assert False, "Shouldn't get here"

        elif mode == "tournament":
            raise NotImplementedError

        elif mode == "rank":
            raise NotImplementedError

        else:
            raise NotImplementedError

    def getMaximumFitness(self):
        return max([chromosome.fitness for chromosome in self.chromosomes])

    def getAverageFitness(self):
        return sum([chromosome.fitness for chromosome in self.chromosomes]) / self.k

    def getTopChromosome(self):
        return max(self.chromosomes, key=lambda c: c.fitness)
