import random
from population import Population

defconfig = {
    "MutationProb": 0.1,
    "K": 20,
    "NQueens": 8,
    "MAX_ITER": int(1e5),
    "pickMode": "wheel",
    "mutateMode": "shift",
    "seed": 1,
}


class GeneticAlgorithm:
    def __init__(self, config=defconfig):
        self.config = config
        random.seed(self.config["seed"])

    def initPool(self):
        self.pool = Population(k=self.config["K"], nqueens=self.config["NQueens"])
        self.generation = 0

    def updatePool(self, retention=0.1):
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
        newPool = (
            sorted(newPool, key=lambda c: c.fitness, reverse=True)[
                : int(self.config["K"] * (1 - retention))
            ]
            + self.pool.chromosomes[
                : self.config["K"] - int(self.config["K"] * (1 - retention))
            ]
        )
        self.generation += 1
        self.pool = Population(chromosomes=newPool)
