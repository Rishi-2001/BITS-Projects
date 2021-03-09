import random
from population import Population

config = {
    "MutationProb": 0.1,
    "K": 20,
    "MAX_ITER": int(1e4),
    "pickMode": "wheel",
    "mutateMode": "swap",
    "seed": 1,
}


class GeneticAlgorithm:
    def __init__(self, inputGraph, config=config):
        self.config = config
        random.seed(self.config["seed"])
        self.graph = inputGraph
        self.history = []

    def initPool(self):
        self.pool = Population(inputGraph=self.graph, k=self.config["K"])
        self.generation = 0
        self.ncities = len(self.graph)

    def updatePool(self):
        newPool = []
        for _ in range(self.config["K"]):
            x, y = (
                self.pool.pick(mode=self.config["pickMode"]),
                self.pool.pick(mode=self.config["pickMode"]),
            )
            child = x.cross(y)
            if random.random() < self.config["MutationProb"]:
                child.mutate(mode=self.config["mutateMode"])
            newPool.append(child)
        self.generation += 1
        self.pool = Population(inputGraph=self.graph, chromosomes=newPool)

    def genStats(self):
        best = self.pool.getBestFitness()
        self.history.append(best)
        return best

    def checkChange(self, n):
        if self.generation > n:
            if len(set(self.history[-n:])) > 1:
                return True
            else:
                return False
        else:
            return True
