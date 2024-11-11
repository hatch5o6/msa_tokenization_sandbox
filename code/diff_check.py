import argparse

def check(
    file1,
    file2
):
    with open(file1) as inf:
        lines1 = [line.strip() for line in inf.readlines()]
    with open(file2) as inf:
        lines2 = [line.strip() for line in inf.readlines()]
    
    assert len(lines1) == len(lines2)

    n_diffs = 0
    for i in range(len(lines1)):
        line1 = lines1[i]
        clean_line1 = line1.replace(", Progressive alignment with LCS", "").replace(", Progressive alignment", "")
        line2 = lines2[i]
        clean_line2 = line2.replace(", Progressive alignment with LCS", "").replace(", Progressive alignment", "")
        if clean_line1 != clean_line2:
            n_diffs += 1
            print(f"-----------{i}-----------")
            print(line1)
            print(line2)

    percent_diff = round(n_diffs / len(lines1) * 100, 2)
    print(f"\n{n_diffs}/{len(lines1)} ({percent_diff}%) lines differ")
        

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", "--file1")
    parser.add_argument("-f2", "--file2")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    check(args.file1, args.file2)