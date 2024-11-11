import argparse
from tqdm import tqdm
import csv
import json

def get_celex_derivation_parses(
    eml_file,
    emw_file
):
    initial_groupings = {}
    eml_lines = read_lines(eml_file)
    emw_lines = read_lines(emw_file)

    all_lemmas = set()
    id2lemma = {}

    for line in tqdm(eml_lines):
        lemma_id = int(line[0])
        lemma = line[1]
        assert lemma_id not in id2lemma
        id2lemma[lemma_id] = lemma
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
        
        if lemma not in initial_groupings:
            initial_groupings[lemma] = []
        initial_groupings[lemma] += morph_parses
        initial_groupings[lemma] = sorted(list(set([item for item in initial_groupings[lemma] if item.strip() != ""])))

    all_lemmas = sorted(list(all_lemmas))

    for row in emw_lines:
        lemma_id = int(row[3])
        lemma = id2lemma[lemma_id]
        if lemma not in initial_groupings:
            # print(lemma)
            initial_groupings[lemma] = [lemma]

    to_pop = []
    for lemma, morph_parses in initial_groupings.items():
        if len(morph_parses) == 0:
            to_pop.append(lemma)
    for key in to_pop:
        initial_groupings.pop(key)
        
    return initial_groupings

    
def get_celex_inflections(
    eml_file,
    emw_file
):
    eml_lines = read_lines(eml_file)
    lemmas = {}
    for row in eml_lines:
        lemma_id = int(row[0])
        lemma = row[1]
        assert lemma_id not in lemmas
        lemmas[lemma_id] = lemma

    emw_lines = read_lines(emw_file)
    inflections = {}
    for row in emw_lines:
        word_form = row[1]
        lemma_id = int(row[3])
        lemma = lemmas[lemma_id]
        if lemma not in inflections:
            inflections[lemma] = []
        if word_form not in inflections[lemma]:
            inflections[lemma].append(word_form)
    
    return inflections

def read_lines(file):
    with open(file) as inf:
        lines = inf.readlines()
    lines = [line.split("\\") for line in lines]
    return lines
    

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--eml", default="/home/hatch5o6/nobackup/archive/data/celex2/english/eml/eml.cd")
    parser.add_argument("--emw", default="/home/hatch5o6/nobackup/archive/data/celex2/english/emw/emw.cd")
    parser.add_argument("--type", choices=["derivations", "inflections"])
    parser.add_argument("--out", "-o")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    if args.type == "inflections":
        morph_parses = get_celex_inflections(args.eml, args.emw)
        with open(args.out, 'w') as outf:
            for lemma, parses in morph_parses.items():
                outf.write(f"{lemma}: {', '.join(parses)}\n")
    elif args.type == "derivations":
        morph_parses = get_celex_derivation_parses(args.eml, args.emw)
        with open(args.out, 'w') as outf:
            for lemma, parses in morph_parses.items():
                outf.write(f"{lemma}: {', '.join(parses)}\n")
        
