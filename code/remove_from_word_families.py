import argparse
import csv


def remove(
    csv_file,
    remove_file
):
    with open(remove_file) as inf:
        remove = set([line.split(":")[0].strip() for line in inf.readlines()])

    out_csv_file = csv_file.replace(".csv", ".removed.csv")

    with open(csv_file, newline="") as inf, open(out_csv_file, "w", newline="") as outf:
        reader = csv.reader(inf)
        writer = csv.writer(outf)
        for row in reader:
            lexeme, cell, phon_form = tuple(row)
            if lexeme not in remove:
                writer.writerow([lexeme, cell, phon_form]) 

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv")
    parser.add_argument("-r", "--remove", default="/home/hatch5o6/LING590R/code/word_families/celex.remove.txt")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    remove(args.csv, args.remove)
