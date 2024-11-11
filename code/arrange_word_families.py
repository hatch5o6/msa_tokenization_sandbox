import argparse
from tqdm import tqdm
import csv
import re
import random

from read_celex_parses import get_celex_derivation_parses, get_celex_inflections
from read_morphynet_parses import get_morphynet_derivation_parses, get_morphynet_inflections


def arrange_families(
    derivation_parses,
    inflections,
    EXCLUDE_TERMS_WITH_WS=False
):
    if EXCLUDE_TERMS_WITH_WS:
        derivation_parses = remove_ws_terms(derivation_parses)
        inflections = remove_ws_terms(inflections)
    
    # for lemma in derivation_parses:
    #     if lemma not in inflections:
    #         print(f"{lemma} not in inflections")
    #     assert lemma in inflections

    all_lemmas = sorted(list(set(list(inflections.keys()) + list(derivation_parses.keys()))))

    lemmas_to_roots = {
        lemma: None
        for lemma in all_lemmas
    }

    print("finding families")
    for lemma in tqdm(all_lemmas):
        roots = []
        # print(lemma)
        depth = 0
        find_families(lemma, derivation_parses, roots, depth)
        # print(roots)
        lemmas_to_roots[lemma] = roots

    print("arranging families")
    families = {}
    for lemma, roots in tqdm(lemmas_to_roots.items()):
        for root in roots:
            if root not in families:
                families[root] = []
            families[root].append(lemma)
            if lemma in inflections:
                families[root] += inflections[lemma]
            families[root] = sorted(list(set(families[root])))

    return families

def remove_ws_terms(structure):
    to_pop = []
    print("Popping")
    for key in structure:
        if " " in key:
            to_pop.append(key)
        # for char in key:
        #     if char.isspace():
        #         to_pop.add(key)
        #         break
    for key in to_pop:
        print(f"\t'{key}'")
        structure.pop(key)
    return structure

def find_families(lemma, derviation_parses, roots, depth):
    # print("lemma", lemma)
    if lemma not in derivation_parses:
        # print(f"'{lemma}' not in derivation parses")
        return

    parses = derivation_parses[lemma]
    for parse in parses:
        if "+" not in parse:
            if parse == lemma:
                roots.append(parse)
            else:
                roots.append(parse)
                roots.append(lemma)
            return
        if depth > 50:
            print(f"Exiting on parse={parse}, depth=={depth}")
            return
        parse = parse.split("+")
        for elem in parse:
            find_families(elem, derviation_parses, roots, depth + 1)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--eml", default="/home/hatch5o6/nobackup/archive/data/celex2/english/eml/eml.cd")
    parser.add_argument("--emw", default="/home/hatch5o6/nobackup/archive/data/celex2/english/emw/emw.cd")
    parser.add_argument("--inf", help="inflection .tsv", default="/home/hatch5o6/nobackup/archive/data/MorphyNet/eng/eng.inflectional.v1.tsv")
    parser.add_argument("--der", help="derivation .tsv", default="/home/hatch5o6/nobackup/archive/data/MorphyNet/eng/eng.derivational.v1.tsv")
    parser.add_argument("--dataset", "-d", required=True, choices=["celex", "morphynet"])
    parser.add_argument("--out", "-o")
    parser.add_argument("--EXCLUDE_TERMS_WITH_WS", action="store_true")
    parser.add_argument("--ADD_WORD_BOUNDARIES", action="store_true")
    parser.add_argument("--csv", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    if args.dataset == "celex":
        derivation_parses = get_celex_derivation_parses(args.eml, args.emw)
        inflections = get_celex_inflections(args.eml, args.emw)
    elif args.dataset == "morphynet":
        with open(args.der) as inf:
            derivations = [tuple([item.strip() for item in line.split("\t")]) for line in inf.readlines()]
        with open(args.inf) as inf:
            inflections = [tuple([item.strip() for item in line.split("\t")]) for line in inf.readlines()]
        derivation_parses = get_morphynet_derivation_parses(derivations, inflections)
        inflections = get_morphynet_inflections(inflections)
    
    word_families = arrange_families(
        derivation_parses,
        inflections,
        EXCLUDE_TERMS_WITH_WS=args.EXCLUDE_TERMS_WITH_WS
    )

    if args.out:
        with open(args.out, "w") as outf:
            for root in sorted(list(word_families.keys())):
                family = word_families[root]
                outf.write(root + "\n")
                for entry in family:
                    outf.write(f"\t{entry}\n")
                outf.write("\n")
    with open(args.csv, "w", newline='') as outf:
        writer = csv.writer(outf)
        writer.writerow(['lexeme', 'cell', 'phon_form'])
        for root in sorted(list(word_families.keys())):
            family = word_families[root]
            for i, word in enumerate(family):
                word = re.sub(r'\s+', ' ', word).strip()
                word = word.replace(" ", "_")
                if args.ADD_WORD_BOUNDARIES:
                    word = "<" + word + ">"
                writer.writerow([root, i, " ".join(word)])
            

