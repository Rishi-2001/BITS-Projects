import random

config = {
    "MutationProb": 0.3,
    "K": 20,
    "NQueens": 8,
    "MAX_ITER": int(1e5),
    "pickMode": "wheel",
    "mutateMode": "shift-swap",
    "retention": 0.2,
    "seed": 4,
}


class Chromosome(list):
    def __init__(self, genes):
        list.__init__(self, genes)
        self.length = len(self)
        self.fitness = self.calculateFitness()

    def calculateFitness(self):
        fitness = 0

        for cx, rx in enumerate(self):
            for cy, ry in enumerate(self):
                if abs(cx - cy) == abs(rx - ry) and not (cx == cy and rx == ry):
                    fitness += 1
                if rx == ry and not cx == cy:
                    fitness += 1
        return 29 - fitness // 2

    def probability(self, alpha=0):
        return 1 / (30 - self.fitness)

    def cross(self, partner):
        junction = random.randint(1, self.length - 2)
        return Chromosome(genes=self[:junction] + partner[junction:])

    def mutate(self, mode="shift"):
        if mode == "shift":
            idx = random.randint(0, self.length - 1)
            self[idx] = random.randint(1, self.length)

        elif mode == "swap":
            idx_1, idx_2 = random.sample(range(self.length), 2)
            self[idx_1], self[idx_2] = self[idx_2], self[idx_1]
        elif mode == "shift-swap":
            self.mutate()
            if random.random() < 0.5:
                self.mutate(mode="swap")
        else:
            raise NotImplementedError
        self.fitness = self.calculateFitness()

    def __str__(self):
        return f"Chromosome : {str([gene for gene in self])}, Fitness = {self.fitness}"

    def display(self):
        columns = []
        for pos in self:
            row = [" * "] * self.length
            row[pos - 1] = " Q "
            columns.append("".join(row))
        return "\n".join(columns)


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


class GeneticAlgorithm:
    def __init__(self, config=config):
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


GAFast = GeneticAlgorithm(config=config)
GAFast.initPool()

while (
    GAFast.pool.getMaximumFitness() < 29
    and GAFast.generation < GAFast.config["MAX_ITER"]
):
    GAFast.updatePool(retention=GAFast.config["retention"])

print(
    f"Solution found in generation {GAFast.generation}:\n{GAFast.pool.getTopChromosome().display()}"
)
