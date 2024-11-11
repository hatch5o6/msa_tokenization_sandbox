import argparse
import csv
import random
import json
import xlsxwriter

def make_subsets(
    csv_file,
    size,
    n_groups
):
    with open(csv_file, newline='') as inf:
        rows = [row for row in csv.reader(inf)]
    header = rows[0]
    data = rows[1:]
    families = {}
    for row in data:
        root = row[1]
        if root not in families:
            families[root] = []
        families[root].append(row)
    
    # print(json.dumps(families, indent=2))

    families = list(families.values())
    random.shuffle(families)

    subsets = []
    start = 0
    for i in range(n_groups):
        subset = families[start:start + size]
        subsets.append(subset)
        start += size

    for i, subset in enumerate(subsets):
        out_file = csv_file.replace(".csv", f".{size}.{i}.csv")
        with open(out_file, "w", newline="") as outf:
            writer = csv.writer(outf)
            writer.writerow(header)
            for family in subset:
                for row in family:
                    writer.writerow(row)


def make_parallel_subsets(
    csv1,
    csv2,
    size,
    n_groups,
    out_csv
):
    with open(csv1, newline='') as inf:
        rows = [row for row in csv.reader(inf)]
    header1 = rows[0]
    data = rows[1:]
    families1 = {}
    for row in data:
        root = row[1]
        row[5], row[6] = f'"{row[5]}"', f'"{row[6]}"'
        if root not in families1:
            families1[root] = []
        families1[root].append(row)

    with open(csv2, newline='') as inf:
        rows = [row for row in csv.reader(inf)]
    header2 = rows[0]
    data = rows[1:]
    families2 = {}
    for row in data:
        root = row[1]
        row[5], row[6] = f'"{row[5]}"', f'"{row[6]}"'
        if root not in families2:
            families2[root] = []
        families2[root].append(row)
    
    families1_keys = sorted(list(families1.keys()))
    families2_keys = sorted(list(families2.keys()))
    assert families1_keys == families2_keys

    selected_families = families1_keys
    random.shuffle(selected_families)

    subsets = []
    start = 0
    for i in range(n_groups):
        subset = selected_families[start:start + size]
        subsets.append(subset)
        start += size

    for i, subset in enumerate(subsets):
        out_file = out_csv.replace(".csv", f".{size}.{i}.csv")
        workbook = xlsxwriter.Workbook(out_file.replace(".csv", ".xlsx"))
        heading_format = workbook.add_format({"bold": True})
        info_even_format = workbook.add_format({"bg_color":"#D0D0D0"})
        info_odd_format = workbook.add_format({"bg_color":"#FFFFF"})
        p_even_format = workbook.add_format({"bg_color":"#A7D9FD"})
        p_odd_format = workbook.add_format({"bg_color":"#F3FAFF"})
        plcs_even_format = workbook.add_format({"bg_color": "#C9F0C9"})
        plcs_odd_format = workbook.add_format({"bg_color": "#F0FFF0"})
        diff_even_format = workbook.add_format({"bg_color": "#FFAAA1"})
        diff_odd_format = workbook.add_format({"bg_color": "#FFD4D0"})
        worksheet = workbook.add_worksheet()
        row_idx = 0

        col_indices_to_write = [0,1,2,3,4,5,6,12,13,14]
        with open(out_file, "w", newline="") as outf:
            writer = csv.writer(outf)
            header = header1 + header2
            writer.writerow(header)
            for col_idx, heading in enumerate(header):
                if col_idx in col_indices_to_write:
                    if col_idx > 6:
                        heading = "ProgressiveLCS " + heading
                        write_col_idx = col_idx - 5
                    else:
                        if col_idx > 3:
                            heading = "Progressive " + heading
                        write_col_idx = col_idx
                    worksheet.write(row_idx, write_col_idx, heading, heading_format)
            for r, root in enumerate(subset):
                family1 = families1[root]
                family2 = families2[root]
                assert len(family1) == len(family2)

                for j in range(len(family1)):
                    row_idx += 1
                    row = family1[j] + family2[j]
                    # assert indices and cells are the same for Progressive and ProgressiveLCS
                    assert row[0] == row[8]
                    assert row[2] == row[10]
                    # assert phon_form for Progressive is phone_form of ProgressiveLCS
                    assert row[3] == row[11]
                    writer.writerow(row)
                    for col_idx in range(len(row)):
                        if r % 2 == 0:
                            if col_idx < 4:
                                format = info_even_format
                            elif col_idx < len(row) / 2:
                                format = p_even_format
                            else:
                                format = plcs_even_format
                        else:
                            if col_idx < 4:
                                format = info_odd_format
                            elif col_idx < len(row) / 2:
                                format = p_odd_format
                            else:
                                format = plcs_odd_format

                        if col_idx in col_indices_to_write:
                            if col_idx > 6:
                                write_col_idx = col_idx - 5
                            else:
                                write_col_idx = col_idx

                            if (write_col_idx == 7 and row[col_idx] != row[4] \
                                or write_col_idx == 8 and row[col_idx] != row[5] \
                                or write_col_idx == 9 and row[col_idx] != row[6]):
                                if r % 2 == 0:
                                    format = diff_even_format
                                else:
                                    format = diff_odd_format
                            
                            worksheet.write(row_idx, write_col_idx, row[col_idx], format)
        worksheet.autofit()
        workbook.close()    
                        



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv")
    parser.add_argument("--csv2")
    parser.add_argument("--size", "-s", type=int, required=True)
    parser.add_argument("--n_groups", "-n", type=int, required=True)
    parser.add_argument("--out", "-o")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    if args.csv and args.csv2:
        make_parallel_subsets(
            args.csv,
            args.csv2,
            args.size,
            args.n_groups,
            args.out
        )
    else:
        make_subsets(args.csv, args.size, args.n_groups)
