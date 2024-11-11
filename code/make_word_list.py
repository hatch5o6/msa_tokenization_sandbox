import argparse
from tqdm import tqdm
import re
from string import punctuation

print("PUNCTUATION")
print(punctuation)

def make_list(
    file,
    out,
    LIMIT
):
    lines = []
    # if LIMIT:
    #     progress = tqdm(total=LIMIT)
    # else:
    #     progress = tqdm(total=10000000)

    print(f"Reading...")
    with open(file) as inf:
        lines = [clean(line) for line in tqdm(inf.readlines())]
        # line = inf.readline()
        # while line:
        #     lines.append(clean(line))
        #     progress.update(1)
        #     if LIMIT and len(lines) >= LIMIT:
        #         break
        #     line = inf.readline()
    
    print("Creating word list")
    text = "\n".join(lines)
    words = text.split()
    word_counts = {}
    for word in words:
        word = word.lower()
        if word not in word_counts:
            word_counts[word] = 0
        word_counts[word] += 1

    words = sorted(
        [
            (count, word) 
            for word, count in word_counts.items()
        ], 
        reverse=True
    )[:LIMIT]

    print("Writing to file")
    with open(out, 'w') as outf:
        for _, word in words:
            outf.write(word.strip() + "\n")

def clean(text):
    for punct in punctuation:
        text = text.replace(punct, " ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True)
    parser.add_argument("--out", "-o", required=True)
    parser.add_argument("--LIMIT", type=int, default=None, help="Pass to limit the number of lines read.")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    make_list(
        args.file,
        args.out,
        args.LIMIT
    )