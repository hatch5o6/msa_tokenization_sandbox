import argparse
import csv
import os
from tqdm import tqdm

def get_rows_w_affix(
    csv_file,
    exponent,
    exp_type
):
    assert exp_type in ["prefix", "infix", "suffix"]

    out_folder = csv_file.replace(".csv", f".{exp_type}")
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    csv_file_name = csv_file.split("/")[-1]
    out_csv_name = csv_file_name.replace(".csv", f".{exp_type}={exponent}.csv")
    out_csv = os.path.join(out_folder, out_csv_name)

    with open(csv_file, newline="") as inf:
        rows = [row for row in csv.reader(inf)]
    header = rows[0]
    columns = {header[i]: i for i in range(len(header))}
    data = rows[1:]

    with open(out_csv, "w", newline="") as outf:
        writer = csv.writer(outf)
        writer.writerow(header)
        for row in data:
            exponents = row[columns["exponents"]].split("-")
            prefix = exponents[0]
            infixes = exponent[1:-1]
            suffix = exponents[-1]
            if exp_type == "prefix":
                if exponent in prefix:
                    writer.writerow(row)
            elif exp_type == "infix":
                for infix in infixes:
                    if exponent in infix:
                        writer.writerow(row)
                        break
            elif exp_type == "suffix":
                if exponent in suffix:
                    writer.writerow(row)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv")
    parser.add_argument("--exponent", "-e")
    parser.add_argument("--exponents_file", "-E")
    parser.add_argument("--type", "-t", required=True, choices=["suffix", "infix", "prefix"])
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    if args.exponents_file:
        with open(args.exponents_file, newline="") as inf:
            rows = [row for row in csv.reader(inf)]
        for row in tqdm(rows):
            exponent = row[0]
            get_rows_w_affix(
                csv_file=args.csv,
                exponent=exponent,
                exp_type=args.type
            )
    if args.exponent:
        get_rows_w_affix(
            csv_file=args.csv,
            exponent=args.exponent,
            exp_type=args.type
        )