from genetic import GeneticAlgorithm
import sys

config = {
    "MutationProb": 0.1,
    "K": 30,
    "MAX_ITER": int(1e4),
    "pickMode": "wheel",
    "mutateMode": "swap",
    "seed": sys.argv[1],
}

Graph = [
    [0, 1e2, 1e2, 1e2, 1e2, 1e2, 0.15, 1e2, 1e2, 0.2, 1e2, 0.12, 1e2, 1e2],
    [1e2, 0, 1e2, 1e2, 1e2, 1e2, 1e2, 0.19, 0.4, 1e2, 1e2, 1e2, 1e2, 0.13],
    [1e2, 1e2, 0, 0.6, 0.22, 0.4, 1e2, 1e2, 0.2, 1e2, 1e2, 1e2, 1e2, 1e2,],
    [1e2, 1e2, 0.6, 0, 1e2, 0.21, 1e2, 1e2, 1e2, 1e2, 0.3, 1e2, 1e2, 1e2],
    [1e2, 1e2, 0.22, 1e2, 0, 1e2, 1e2, 1e2, 0.18, 1e2, 1e2, 1e2, 1e2, 1e2],
    [1e2, 1e2, 0.4, 0.21, 1e2, 0, 1e2, 1e2, 1e2, 1e2, 0.37, 0.6, 0.26, 0.9],
    [0.15, 1e2, 1e2, 1e2, 1e2, 1e2, 0, 1e2, 1e2, 1e2, 0.55, 0.18, 1e2, 1e2],
    [1e2, 0.19, 1e2, 1e2, 1e2, 1e2, 1e2, 0, 1e2, 0.56, 1e2, 1e2, 1e2, 0.17],
    [1e2, 0.4, 0.2, 1e2, 0.18, 1e2, 1e2, 1e2, 0, 1e2, 1e2, 1e2, 1e2, 0.6],
    [0.2, 1e2, 1e2, 1e2, 1e2, 1e2, 1e2, 0.56, 1e2, 0, 1e2, 0.16, 1e2, 0.5],
    [1e2, 1e2, 1e2, 0.3, 1e2, 0.37, 0.55, 1e2, 1e2, 1e2, 0, 1e2, 0.24, 1e2],
    [0.12, 1e2, 1e2, 1e2, 1e2, 0.6, 0.18, 1e2, 1e2, 0.16, 1e2, 0, 0.4, 1e2],
    [1e2, 1e2, 1e2, 1e2, 1e2, 0.26, 1e2, 1e2, 1e2, 1e2, 0.24, 0.4, 0, 1e2],
    [1e2, 0.13, 1e2, 1e2, 1e2, 0.9, 1e2, 0.17, 0.6, 0.5, 1e2, 1e2, 1e2, 0],
]

GAFast = GeneticAlgorithm(inputGraph=Graph, config=config)
GAFast.initPool()
bestFitness = GAFast.genStats()

solution = GAFast.pool.getBestChromosome()
print(bestFitness)

while GAFast.generation < GAFast.config["MAX_ITER"]:
    GAFast.updatePool()
    prev_best, bestFitness = bestFitness, GAFast.genStats()
    if bestFitness > prev_best:
        solution = GAFast.pool.getBestChromosome()

bestFitness = max(GAFast.history)

print(
    f"Solution found in generation {GAFast.history.index(bestFitness)+1}:\n{solution.display()}\nFitness: {solution.fitness}"
)
