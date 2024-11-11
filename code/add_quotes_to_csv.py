import argparse
import csv
from tqdm import tqdm

def add_quotes(
    csv_f,
    out_f,
    fields = None
):
    
    with open(csv_f, newline="") as inf:
        data = [row for row in csv.reader(inf)]
    header = data[0]
    header_dict = {i: header[i] for i in range(len(header))}
    if fields:
        fields = [f.strip() for f in fields.split(",")]
    else:
        fields = [f for f in header]
    rows = data[1:]
    print(f"writing to {out_f}")
    with open(out_f, "w", newline="") as outf:
        writer = csv.writer(outf)
        writer.writerow(header)
        for row in tqdm(rows):
            for v, value in enumerate(row):
                heading = header_dict[v]
                if heading in fields:
                    row[v] = f"\"{value}\""
            writer.writerow(row)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv")
    parser.add_argument("--out")
    parser.add_argument("--fields", "-f", help="fields to add quotes arround, comma-delimited. If None, then all fields will get quotes.")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    out = args.out
    if not out:
        out = args.csv.replace(".csv", ".q.csv")
    add_quotes(args.csv, out, args.fields)
