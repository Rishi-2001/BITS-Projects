import random


class Chromosome(list):
    def __init__(self, inputGraph, genes):
        self.graph = inputGraph
        list.__init__(self, genes)
        self.length = len(self)
        self.fitness = self.calculateFitness()

    def calculateFitness(self):
        fitness = 0
        for city in range(self.length):
            start, end = self[city], self[(city + 1) % self.length]
            fitness += self.graph[start][end]
        return 1 / fitness

    def cross(self, partner):
        child = [None] * self.length
        x, y = random.sample(range(1, self.length), 2)
        x, y = min(x, y), max(x, y)
        child[x:y] = self[x:y]
        order = list(reversed([gene for gene in partner if gene not in child]))
        for idx in range(self.length):
            if child[idx] is None:
                child[idx] = order.pop()
        return Chromosome(inputGraph=self.graph, genes=child)

    def mutate(self, mode="swap"):
        if mode == "swap":
            x, y = random.sample(range(self.length), 2)
            self[x], self[y] = self[y], self[x]
        self.fitness = self.calculateFitness()

    def __str__(self):
        return f"Chromosome : {str([gene for gene in self])}, Fitness = {self.fitness}"

    def display(self):
        return (" --> ").join([chr(ord("A") + city) for city in (self + [self[0]])])
