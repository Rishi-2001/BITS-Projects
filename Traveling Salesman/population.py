import random
from chromosome import Chromosome


class Population:
    def __init__(self, inputGraph, k=20, chromosomes=None):

        self.graph = inputGraph
        if chromosomes is None:
            self.k = k
            self.ncities = len(self.graph)
            self.chromosomes = [
                Chromosome(self.graph, list(range(self.ncities))) for _ in range(k)
            ]
        else:
            self.k = len(chromosomes)
            self.ncities = len(self.graph)
            self.chromosomes = chromosomes

    def pick(self, mode="tournament", tournament_size=2):
        if mode == "wheel-tournament":
            return self.pick(mode=random.choice(["tournament", "wheel"]))

        if mode == "wheel":
            return random.choices(
                population=self.chromosomes,
                k=1,
                weights=[c.fitness for c in self.chromosomes],
            )[0]

        elif mode == "tournament":
            participants = random.sample(self.chromosomes, tournament_size)
            return max(participants, key=lambda c: c.fitness)

        else:
            raise NotImplementedError

    def getBestFitness(self):
        return max([chromosome.fitness for chromosome in self.chromosomes])

    def getBestChromosome(self):
        return max(self.chromosomes, key=lambda c: c.fitness)
