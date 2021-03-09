from dataGen import CircuitGenerator as CG
from random import choice, seed
import argparse

# CLI Parser
parser = argparse.ArgumentParser(description="Data Generation for Artificial Crcuits")
parser.add_argument("--x_lim", "-x", help="Enter X limit", type=int, default=5)

parser.add_argument("--y_lim", "-y", help="Enter Y limit", type=str, default=5)

parser.add_argument(
    "--seed", "-s", help="Enter seed", type=int, default=22,
)
parser.add_argument(
    "--num", "-n", help="Enter number of samples", type=int, default=10000
)
parser.add_argument("--scale", help="Enter scale of image", type=int, default=3)
parser.add_argument(
    "--bbox", "-b", help="True to plot bounding boxes", type=bool, default=False
)

args = parser.parse_args()
seed(args.seed)

cg = CG(x_lim=args.x_lim, y_lim=args.y_lim, scale=args.scale)
for i in range(args.num):
    pAdjs, pDiags = choice([0.4, 0.5, 0.6, 0.7]), choice([0.2, 0.3, 0.4, 0.5])
    lines = cg.generateLines(pAdjs=pAdjs, pDiags=pDiags)
    canvas = cg.generateCircuit(lines, False)
    canvas.save(f"0X{int(10*pAdjs)}_0X{int(10*pDiags)}_{i}.png", boxes=args.bbox)
