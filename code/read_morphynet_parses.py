import argparse


def get_morphynet_derivation_parses(
    derivations,
    inflections
):
    morph_parses = {}
    for root, lemma, _, _, affix, type in derivations:
        if affix.strip() == "": continue

        if lemma not in morph_parses:
            morph_parses[lemma] = []
        if type == "suffix":
            morph_parses[lemma].append(f"{root}+{affix}")
        else:
            morph_parses[lemma].append(f"{affix}+{root}")
        morph_parses[lemma] = sorted(list(set(morph_parses[lemma])))

    for lemma, inflection, _, _ in inflections:
        if lemma not in morph_parses:
            morph_parses[lemma] = [lemma]

    return morph_parses

def get_morphynet_inflections(
    inflections
):
    inflection_families = {}
    for lemma, inflection, _, _ in inflections:
        if lemma not in inflection_families:
            inflection_families[lemma] = [lemma]
        if inflection not in inflection_families[lemma]:
            inflection_families[lemma].append(inflection)
    return inflection_families

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inf", help="inflection .tsv", default="/home/hatch5o6/nobackup/archive/data/MorphyNet/eng/eng.inflectional.v1.tsv")
    parser.add_argument("--der", help="derivation .tsv", default="/home/hatch5o6/nobackup/archive/data/MorphyNet/eng/eng.derivational.v1.tsv")
    parser.add_argument("--type", choices=["derivations", "inflections"])
    parser.add_argument("--out", "-o")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    with open(args.inf) as inf:
        inflections = [tuple([item.strip() for item in line.split("\t")]) for line in inf.readlines()]
    if args.type == "derivations":
        with open(args.der) as inf:
            derivations = [tuple([item.strip() for item in line.split("\t")]) for line in inf.readlines()]
        print(f"{len(derivations)} derviations")
        types = set()
        for l, line in enumerate(derivations):
            if len(line) != 6:
                print(l, line)
            types.add(line[-1].strip())
        types = sorted(list(types))
        print("TYPES:", types)
        morph_parses = get_morphynet_derivation_parses(derivations, inflections)
        with open(args.out, 'w') as outf:
            for lemma, parses in morph_parses.items():
                outf.write(f"{lemma}: {', '.join(parses)}\n")
    elif args.type == "inflections":
        print(f"{len(inflections)} inflections")
        morph_parses = get_morphynet_inflections(inflections)
        with open(args.out, 'w') as outf:
            for lemma, parses in morph_parses.items():
                outf.write(f"{lemma}: {', '.join(parses)}\n")

