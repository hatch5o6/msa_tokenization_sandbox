import argparse
from tqdm import tqdm
import csv
import json

def get_word_families(
    eml_file,
    emw_file
):
    initial_groupings = {}
    eml_lines = read_lines(eml_file)
    emw_lines = read_lines(emw_file)

    all_lemmas = set()

    for line in tqdm(eml_lines):
        i = line[0]
        lemma = line[1]
        if len(lemma.split()) > 1:
            continue
        all_lemmas.add(lemma)

        morph_parses = []
        morph_parse_idx = 11
        while morph_parse_idx < len(line):
            morph_parses.append(line[morph_parse_idx])
            morph_parse_idx += 19
        # if len(morph_parses) > 1:
        #     print(morph_parses)

        if i not in initial_groupings:
            initial_groupings[i] = {"lemma": lemma, "forms": [], "morph_parses": morph_parses}
        else:
            print(f"lemma id {i} already exits")
            if lemma in initial_groupings[i]:
                print(f"lemma {lemma} already in family!")

        if len(morph_parses) == 0:
            initial_groupings[i]["forms"].append(lemma)

    for line in tqdm(emw_lines):
        i = line[3]
        word_form = line[1]
        if len(word_form.split()) > 1:
            continue
        if i not in initial_groupings:
            print("creating word family from word form", word_form)
            initial_groupings[i] = {"lemma": word_form, "forms": [], "morph_parses": []}
        initial_groupings[i]["forms"].append(word_form)


    all_morph_parses = {}
    for i, grouping in tqdm(initial_groupings.items()):
        assert grouping["lemma"] is not None
        lemma = grouping["lemma"]
        morph_parses = [parse.split("+") for parse in grouping["morph_parses"]]
        if lemma not in all_morph_parses:
            all_morph_parses[lemma] = []
        for parse in morph_parses:
            if parse not in all_morph_parses[lemma]:
                all_morph_parses[lemma].append(parse)
    with open("all_morph_parses.json", "w") as outf:
        outf.write(json.dumps(all_morph_parses, ensure_ascii=False, indent=2))
    

    word_families = {}
    for i, grouping in tqdm(initial_groupings.items()):
        assert grouping["lemma"] is not None
        lemma = grouping["lemma"]
        morph_parses = grouping["morph_parses"]
        if len(morph_parses) == 0:
            if lemma not in word_families:
                word_families[lemma] = []
            word_families[lemma] += grouping["forms"]
        else:
            for parse in morph_parses:
                components = parse.split("+")
                for component in components:
                    # seeing if the component is a lemma, and if so, adding it to that lemma's word family (as opposed to creating a family for the compound word)
                    if component in all_lemmas:
                        if component not in word_families:
                            word_families[component] = []
                        word_families[component].append(lemma)
    
    # NEEDS FIXING
    # merges wolf, wolfbane, bane
    # word_lists = {}
    # for lemma, word_family in word_families.items():
    #     for word in word_family:
    #         if word not in word_lists:
    #             word_lists[word] = []
    #         else:
    #             word_lists[word] = list(set(word_lists[word] + word_family))
    #             word_families[lemma] = word_lists[word]
    
    return word_families
    

def read_lines(file):
    with open(file) as inf:
        lines = inf.readlines()
    lines = [line.split("\\") for line in lines]
    return lines
    

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--eml", default="/home/hatch5o6/nobackup/archive/data/celex2/english/eml/eml.cd")
    parser.add_argument("--emw", default="/home/hatch5o6/nobackup/archive/data/celex2/english/emw/emw.cd")
    parser.add_argument("--out", "-o")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    word_families = get_word_families(args.eml, args.emw)
    with open(args.out, 'w', newline='') as outf:
        writer = csv.writer(outf)
        for i, word_family in word_families.items():
            print(type(word_family))
            print(word_family)
            writer.writerow(list(set(word_family)))
