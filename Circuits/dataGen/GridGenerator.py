from random import randint, random, sample, shuffle, seed, choice


class GridGenerator:
    def __init__(self, x_lim=10, y_lim=10, scale=5, random_state=42):
        self.seed = random_state
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.scale = scale
        seed(self.seed)
        self.grid = self.gridInit()
        self.adjacentGrid = self.adjacentInit()

    def gridInit(self):
        gridPoints = []
        for x in range(self.x_lim):
            for y in range(self.y_lim):
                gridPoints.append([x, y])
        return gridPoints

    def adjacentInit(self):
        adjacentGrid = []
        for y in range(self.y_lim):
            adjacentGrid.extend([([x, y], [(x + 1), y]) for x in range(self.x_lim - 1)])
        for x in range(self.x_lim):
            adjacentGrid.extend([([x, y], [x, (y + 1)]) for y in range(self.y_lim - 1)])
        return adjacentGrid

    def diagonalInit(self):
        diagonalGrid = []
        for x in range(self.x_lim - 1):
            for y in range(self.y_lim - 1):
                diagonalGrid.append(
                    choice([([x, y], [x + 1, y + 1]), ([x + 1, y], [x, y + 1])])
                )
        return diagonalGrid

    def RandomAdjacentInit(self, numAdjs):
        return sample(self.adjacentGrid, numAdjs)

    def RandomDiagonalInit(self, allDiags, numDiags):
        return sample(allDiags, numDiags)

    def generatePadding(self):
        return [
            ([-0.25, 0], [0, 0]),
            ([0, -0.25], [0, 0]),
            ([self.x_lim - 1, self.y_lim - 1], [self.x_lim - 0.75, self.y_lim - 1]),
            ([self.x_lim - 1, self.y_lim - 1], [self.x_lim - 1, self.y_lim - 0.75]),
        ]

    def generateLines(self, pAdjs=0.5, pDiags=0.3):
        diagonalGrid = self.diagonalInit()
        numAdjs = int(pAdjs * len(self.adjacentGrid))
        numDiags = int(pDiags * len(diagonalGrid))
        grid = (
            self.RandomDiagonalInit(diagonalGrid, numDiags)
            + self.RandomAdjacentInit(numAdjs)
            + self.generatePadding()
        )
        scaledGrid = []
        for line in grid:
            scaledGrid.append(
                (
                    [line[0][0] * self.scale, line[0][1] * self.scale],
                    [line[1][0] * self.scale, line[1][1] * self.scale],
                )
            )
        return scaledGrid
