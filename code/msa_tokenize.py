import argparse
import os
import csv
import copy
import json

class MSATokenizer():
    def __init__(self, model, cache_path="msa_cache/msa_parses.csv"):
        self.cache_path = cache_path
        cache_parent_dir = "/".join(self.cache_path.split("/")[:-1])
        if not os.path.exists(cache_parent_dir):
            os.mkdir(cache_parent_dir)

        stems = self.read_exp(model, exp_type="stem")
        prefixes = self.read_exp(model, exp_type="prefix")
        infixes = self.read_exp(model, exp_type="infix")
        suffixes = self.read_exp(model, exp_type="suffix")

        self.exponents = Exponents(
            stems=stems, 
            prefixes=prefixes, 
            infixes=infixes, 
            suffixes=suffixes
        )

    def read_exp(self, model_dir, exp_type="prefix"):
        f = os.path.join(model_dir, f"{exp_type}.csv")
        with open(f, newline="") as inf:
            reader = csv.reader(inf)
            exps = {stem: int(c) for stem, c in reader}
        return exps

    def tokenize_word(self, word):
        empty = ""
        word_chars = [empty] + [c for c in word] + [empty]
        parses = [{
            "ID": 0, 
            "prefix": [""], 
            "prefix_score": [0], 
            "stem": "", 
            "stem_score": 0, 
            "suffix": [""], 
            "suffix_score": [0], 
            "state": "prefix",
            "state_idx": 0
        }]

        next_parse_id = 0
        for i, c in enumerate(word_chars):
            # for p, parse in enumerate(parses):
            new_parses = []
            for p, parse in enumerate(parses):
                if parse["state"] in ["dead", "done"]: continue
                state = parse["state"]
                if state in ["prefix", "suffix", "infix"]:
                    state_idx = parse["state_idx"]
                    parse[state][state_idx] += c
                    substr = parse[state][state_idx]
                else:
                    parse[state] += c
                    substr = parse[state]
                
                state_score = self.exponents.get(state).get_score(substr)

                if state in ["prefix", "suffix", "infix"]:
                    while state_idx < len(parse[f"{state}_score"]) - 1:
                        parse[f"{state}_score"].append(0)
                    parse[f"{state}_score"][state_idx] = state_score
                else:
                    parse[f"{state}_score"] = state_score

                if state_score == None:
                    parse["state"] = "dead"

                parses[p] = parse

                # if prefix or suffix, make a new parse at the same state
                if parse["state"] in ["prefix", "suffix"]:
                    new_same_state_parse = copy.deepcopy(parse)
                    next_parse_id += 1
                    new_same_state_parse["ID"] = next_parse_id
                    new_same_state_parse["state_idx"] += 1

                # make a new parse at the next state
                new_next_state_parse = copy.deepcopy(parse)
                next_parse_id += 1
                new_next_state_parse["ID"] = next_parse_id
                if new_next_state_parse["state"] == "prefix":
                    new_next_state_parse["state"] = "stem"
                elif new_next_state_parse["state"] == "stem":
                    new_next_state_parse["state"] = "suffix"
                elif new_next_state_parse["state"] == "suffix":
                    new_next_state_parse["state"] = "dead"
                new_parses.append(new_next_state_parse)
            parses += new_parses

        refined_parses = []
        n_valid_parses = 0
        for p, parse in enumerate(parses):
            hypothesis_word = "".join(parse["prefix"]) + parse["stem"] + "".join(parse["suffix"])
            if parse["state"] == "dead":
                score = 0
            elif hypothesis_word != word:
                score = 0
            elif sum(parse["prefix_score"]) == 0 or sum(parse["suffix_score"]) == 0:
                score = 0
            else:
                n_valid_parses += 1
                score = sum(parse["prefix_score"]) + parse["stem_score"] + sum(parse["suffix_score"])
                parse["score"] = score
                # parse = [item for item in [parse["prefix"], parse["stem"], parse["suffix"]] if item]
                refined_parses.append((score, json.dumps(parse, ensure_ascii=False)))
        refined_parses.sort(reverse=True)
        for score, parse in refined_parses:
            print("PARSE", f"score: {score}", json.dumps(json.loads(parse), indent=2, ensure_ascii=False))

        print("---------------------------------------")
        if len(refined_parses) > 0:
            best_parse_score, best_parse = refined_parses[0]
            best_parse = json.loads(best_parse)
            print("N PARSES", len(refined_parses))
            print("VALID PARSES", n_valid_parses)
            print("BEST PARSE:", best_parse_score, json.dumps(best_parse, ensure_ascii=False, indent=2))
        else:
            print("NO PARSES")


class Exponents():
    def __init__(
        self,
        stems: dict,
        prefixes: dict,
        infixes: dict,
        suffixes: dict
    ):
        """
        stems, prefixes, infixes, suffixes: dicts mapping vocab item (exp) -> score
        """
        self.stems = MSATrie(stems)
        self.prefixes = MSATrie(prefixes)
        self.infixes = MSATrie(infixes)
        self.suffixes = MSATrie(suffixes)

    def get(self, state):
        assert state in ["stem", "prefix", "infix", "suffix"]
        if state == "stem":
            return self.stems
        elif state == "prefix":
            return self.prefixes
        elif state == "infix":
            return self.infixes
        elif state == "suffix":
            return self.suffixes


class MSATrie():
    def __init__(
        self, 
        vocabulary: dict
    ):
        """
        vocabulary maps vocab item (exp) -> score
        """
        root_tok = "<ROOT>"
        self.root = TrieNode(char=root_tok, path=[root_tok])
        if vocabulary:
            for exp, score in vocabulary.items():
                self.put(exp, score)

    def put(self, exp, score):
        if exp == "":
            exp = [""]
        node = self.root
        for i, c in enumerate(exp):
            if c not in node.branch:
                node.branch[c] = TrieNode(char=c, path=node.path + [c])
            node = node.branch[c]
            if i == len(exp) - 1:
                assert node.score in [0, score]
                node.score = score
            
    def get(self, exp):
        if exp == "":
            exp = [""]
        node = self.root
        for i, c in enumerate(exp):
            if c in node.branch:
                node = node.branch[c]
            else:
                node = TrieNode()
                break
        
        return node

    def get_score(self, exp):
        node = self.get(exp)
        return node.score

class TrieNode():
    def __init__(
        self, 
        char: str = None,
        path: list = None
    ):
        self.char = char
        self.path = path
        if self.char == None:
            self.score = None
        else:
            self.score = 0
        self.branch = {}

    def __str__(self):
        return f"char: \'{self.char}\', score: \'{self.score}\', path: \'{self.path}\',  branch: \'{self.branch}\'"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--word", default="runs")
    parser.add_argument("-m", "--model", default="msa_model")
    parser.add_argument("-t", "--text")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    tokenizer = MSATokenizer(model=args.model)
    tokenizer.tokenize_word(args.word)

