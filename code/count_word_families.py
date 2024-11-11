import argparse
import csv
from tqdm import tqdm

def count(
    csv_file,
    out
):
    with open(csv_file, newline="") as inf:
        print("reading")
        rows = [row for row in tqdm(csv.reader(inf))]
    header = rows[0]
    counts = {}
    data = rows[1:]
    print("counting")
    for row in tqdm(data):
        lexeme, cell, phon_form = tuple(row)
        if lexeme not in counts:
            counts[lexeme] = 0
        counts[lexeme] += 1

    counts = sorted([(count, root) for root, count in counts.items()], reverse=True)
    with open(out, 'w') as outf:
        for count, root in counts:
            outf.write(f"{root}: {count}\n")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    if args.out:
        out = args.out
    else:
        out = args.csv.replace(".csv", ".counts.txt")
    count(args.csv, out)
