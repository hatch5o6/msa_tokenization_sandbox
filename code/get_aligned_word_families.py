import argparse
import csv

def main(
    word_families_csv,
    out_file
):
    families = {}
    

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv")
    parser.add_argumnet("-o", "--out")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    main(args.csv, args.out)