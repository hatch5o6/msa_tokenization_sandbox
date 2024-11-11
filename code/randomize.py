import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f")
args = parser.parse_args()

with open(args.file) as inf:
    words = inf.read().split()
random.shuffle(words)
with open(args.file.replace(".txt", ".random.txt"), "w") as outf:
    outf.write("\n".join(words) + "\n")