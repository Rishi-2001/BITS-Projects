from genetic import GeneticAlgorithm

config = {
    "MutationProb": 0.3,
    "K": 20,
    "NQueens": 8,
    "MAX_ITER": int(1e5),
    "pickMode": "wheel",
    "mutateMode": "shift-swap",
    "retention": 0.2,
    "seed": 1,
}

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
