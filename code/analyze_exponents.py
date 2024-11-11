import argparse
import csv
from collections import Counter

def analyze(
    csv_file,
    out_file,
    threshold
):
    with open(csv_file, newline="") as inf:
        rows = [row for row in csv.reader(inf)]
    columns = {rows[0][i]: i for i in range(len(rows[0]))}
    data = rows[1:]
    stems = Counter()
    exponents = Counter()
    total_raw_exponents = 0
    total_unique_exponents = 0
    for row in data:
        word_stem = row[columns["stem"]]
        word_stem = remove_dashes(word_stem)
        stems[word_stem] += 1
        word_exponents = row[columns["exponents"]]
        word_exponents = remove_dashes(word_exponents)
        word_exponents = [exp.strip() for exp in word_exponents.split("-") if exp.strip() != ""]
        total_raw_exponents += len(word_exponents)
        for exp in word_exponents:
            exponents[exp] += 1

    total_unique_exponents = len(exponents)
    exponent_tuples = sorted([(c, c/total_raw_exponents, e) for e, c in exponents.items()], reverse=True)
    query_exp_tuples = [exp for exp in exponent_tuples if exp[1] >= threshold]
    print(f"{len(query_exp_tuples)} query exponents")
    query_exp_substr_counts = Counter()
    for _, _, q_exp in query_exp_tuples:
        for _, _, exp in exponent_tuples:
            if q_exp in exp:
                query_exp_substr_counts[q_exp] += 1
    query_exp_substr_counts_tuples = sorted(
        [
            (count, exp) 
            for exp, count in query_exp_substr_counts.items()
        ],
        reverse=True
    )

    print("query_exp_substr_counts")
    for count, exp in query_exp_substr_counts_tuples:
        print(f"'{exp}':'{count}'")
    with open(out_file, "w", newline="") as outf:
        writer = csv.writer(outf)
        for count, exp in query_exp_substr_counts_tuples:
            writer.writerow([exp, count])

    print("total raw exponents", total_raw_exponents)
    print("total unique exponents", total_unique_exponents)


def analyze_affixes(
    csv_file,
    out_file,
    threshold
):
    with open(csv_file, newline="") as inf:
        rows = [row for row in csv.reader(inf)]
    columns = {rows[0][i]: i for i in range(len(rows[0]))}
    print("COLUMNS", columns)
    data = rows[1:]
    stems_ct = Counter()
    prefixes_ct = Counter()
    infixes_ct = Counter()
    suffixes_ct = Counter()
    prefixes = []
    infixes = []
    suffixes = []
    for r, row in enumerate(data):
        # print(f"-----------({r})-----------")
        # print(row)
        word_stem = row[columns["stem"]]
        word_stem = remove_dashes(word_stem)
        stems_ct[word_stem] += 1
        word_exponents = row[columns["exponents"]].split("-")
        word_prefix = word_exponents[0].strip()
        word_infixes = [e.strip() for e in word_exponents[1:-1] if e.strip() != ""]
        # word_infixes = [e.strip() for e in word_exponents[1:-1]]
        word_suffix = word_exponents[-1].strip()
        # print(f"prefix: '{word_prefix}'")
        # print(f"infixes: {word_infixes}")
        # print(f"suffix: '{word_suffix}'")
        # if r > 1000 and r < 1020:
        #     break

        if word_prefix != "":
            prefixes.append(word_prefix)
            prefixes_ct[word_prefix] += 1
        infixes += word_infixes
        for e in word_infixes:
            infixes_ct[e] += 1
        if word_suffix != "":
            suffixes.append(word_suffix)
            suffixes_ct[word_suffix] += 1
    
    # prefixes
    prefix_file = out_file.replace("{label}", "prefix.raw")
    write_raw_ct(prefixes_ct, out_file=prefix_file)

    # infixes
    infix_file = out_file.replace("{label}", "infix.raw")
    write_raw_ct(infixes_ct, out_file=infix_file)

    # suffixes
    suffix_file = out_file.replace("{label}", "suffix.raw")
    write_raw_ct(suffixes_ct, out_file=suffix_file)

    # stems
    stems_file = out_file.replace("{label}", "stems.raw")
    write_raw_ct(stems_ct, out_file=stems_file)

    # get_affix_substr_cts(
    #     exponents=prefixes_ct, 
    #     threshold=threshold, 
    #     out_file=out_file.replace(".csv", ".prefixes.substr.csv"), 
    #     exp_type="prefix"
    # )
    # get_affix_substr_cts(
    #     exponents=infixes_ct, 
    #     threshold=threshold, 
    #     out_file=out_file.replace(".csv", ".infixes.substr.csv"), 
    #     exp_type="infix"
    # )
    # get_affix_substr_cts(
    #     exponents=suffixes_ct, 
    #     threshold=threshold, 
    #     out_file=out_file.replace(".csv", ".suffixes.substr.csv"), 
    #     exp_type="suffix"
    # )
     
def write_raw_ct(exponent_cts, out_file):
    exp_list = sorted([(ct, exp) for exp, ct in exponent_cts.items()], reverse=True)
    with open(out_file, "w", newline="") as outf:
        writer = csv.writer(outf)
        for count, exp in exp_list:
            writer.writerow([exp, count])

def get_affix_substr_cts(exponents, threshold, out_file, exp_type="prefix"):
    # exponents is Counter object of affixes

    assert exp_type in ["prefix", "infix", "suffix"]

    total_raw_exponents = sum(list(exponents.values()))
    total_unique_exponents = len(exponents)
    exponent_tuples = sorted([(c, c/total_raw_exponents, e) for e, c in exponents.items()], reverse=True)
    query_exp_tuples = [exp for exp in exponent_tuples if exp[1] >= threshold]
    print(f"{len(query_exp_tuples)} query {exp_type}es")
    query_exp_substr_counts = Counter()
    for _, _, q_exp in query_exp_tuples:
        for _, _, exp in exponent_tuples:
            # if exp_type == "prefix":
            #     condition = exp.startswith(q_exp)
            # elif exp_type == "infix":
            #     condition = q_exp in exp
            # elif exp_type == "suffix":
            #     condition = exp.endswith(q_exp)
            # if condition:
            if q_exp in exp:
                query_exp_substr_counts[q_exp] += 1
    query_exp_substr_counts_tuples = sorted(
        [
            (count, exp) 
            for exp, count in query_exp_substr_counts.items()
        ],
        reverse=True
    )

    # print(f"query_exp_({exp_type})_substr_counts")
    # for count, exp in query_exp_substr_counts_tuples:
    #     print(f"'{exp}':'{count}'")
    with open(out_file, "w", newline="") as outf:
        writer = csv.writer(outf)
        for count, exp in query_exp_substr_counts_tuples:
            writer.writerow([exp, count])

    # print(f"total raw {exp_type}", total_raw_exponents)
    # print(f"total unique {exp_type}", total_unique_exponents)

def remove_dashes(word):
    word = word.strip()
    if word.startswith("-"):
        word = word[1:]
    if word.endswith("-"):
        word = word[:-1]
    return word.strip()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="morphalign results")
    parser.add_argument("--out", "-o")
    parser.add_argument("--threshold", type=float, default=0.0001, help="top ratio of initial exponents to check against all others")
    return parser.parse_args()

if __name__ ==  "__main__":
    args = get_args()
    if args.out:
        out = args.out
    else:
        out = args.csv.replace(".csv", ".{label}.csv")
    analyze_affixes(args.csv, out, args.threshold)