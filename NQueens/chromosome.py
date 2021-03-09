import random


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
