import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required=True)
parser.add_argument("-o", "--out")
args = parser.parse_args()

f = args.file
if args.out:
    out_f = args.out
else:
    out_f = f.replace(".csv", ".nodash.csv")

with open(f, newline="") as inf:
    rows = [row for row in csv.reader(inf)]
header = rows[0]
data = rows[1:]

with open(out_f, "w", newline="") as outf:
    writer = csv.writer(outf)
    writer.writerow(header)
    for row in data:
        phon_form = row[3]
        if "-" not in phon_form:
            writer.writerow(row)
