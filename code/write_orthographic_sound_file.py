import csv
import argparse
from string import punctuation
import re

default_text = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" + punctuation

def write(
    text_file,
    out,
    ADD_FEATURES
):
    if text_file == "DEFAULT":
        text = default_text
    else:
        with open(text_file) as inf:
            text = inf.read()
    
    characters = sorted([
        char for char in set(text)
        if not re.fullmatch(r'\s', char)
    ])
    
    with open(out, "w", newline='') as outf:
        writer = csv.writer(outf)
        
        header = ['sound_id', 'tier', 'value']
        if ADD_FEATURES:
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            for char in alphabet:
                header.append(char)
            writer.writerow(header)
            for char in characters:
                row = [char, 'segmental', char]
                for feature in alphabet:
                    if char.lower() == feature:
                        row.append(1)
                    else:
                        row.append(0)
                writer.writerow(row)
        else:
            writer.writerow(header)
            for char in characters:
                writer.writerow([char, 'segmental', char])

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text_file", "-t", default="DEFAULT", help="")
    parser.add_argument("--out", "-o")
    parser.add_argument("--ADD_FEATURES", action="store_true", help="adds common feature to capital and lowercase version of each letter")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    write(args.text_file, args.out, args.ADD_FEATURES)