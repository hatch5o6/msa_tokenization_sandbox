import argparse
import csv
from tqdm import tqdm
import copy
import os
import re

# given list of affixes (.prefix/infix/suffix.raw.csv) and frequencies
# make hypotheses on splitting affixes into subaffixes i.e. ization -> iz+at+ion

def run(
    csv_file,
    STOP,
    ADD_NEW_AFFIXES,
    score
):
    if score == "max":
        score_function = max
    elif score == "sum":
        score_function = sum

    with open(csv_file, newline="") as inf:
        data = []
        for row in csv.reader(inf):
            exponent, count = tuple(row)
            count = int(count)
            data.append((count, exponent))
    data.sort(reverse=True)

    iteration = -1
    while True:
        iteration += 1
        visited = []
        parses = {}
        parses_with_scores = {}
        selected_parses = {}
        exp_counts = {exp: count for count, exp in data}
        exp_counts.update({None: 0})

        # potential_new_exps_startswith = {}
        # potential_new_exps_endswith = {}

        total = len(data)
        if STOP:
            total=STOP

        print("Iteration", iteration)
        for i, (_, exp) in tqdm(enumerate(data), total=total):
            visited.append(exp)
            default_parse = (exp, None)
            parses[exp] = [default_parse]
            parses_with_scores[exp] = []
            was_parsed = False
            for token_a in visited:
                parsed_with_token_b = False
                for token_b in visited:
                    # if token_a + token_b comprises the whole exponent
                    if token_a + " " + token_b == exp:
                        was_parsed = True
                        parsed_with_token_b = True
                        parse = (token_a, token_b)
                        parses[exp].append(parse)

                        # select parse
                        parse_scores = []
                        # parses_with_scores[exp] = []
                        for a, b in parses[exp]:
                            # print(exp_counts)
                            hyp_exp_counts = copy.deepcopy(exp_counts)
                            if exp in selected_parses:
                                (old_a, old_b), old_parse_score, old_exp_count_diff = selected_parses[exp]
                                hyp_exp_counts[old_a] -= old_exp_count_diff
                                hyp_exp_counts[old_b] -= old_exp_count_diff

                            # print("hyp_exp_counts", hyp_exp_counts)
                            cur_exp_count_diff = hyp_exp_counts[exp]
                            hyp_exp_counts[a] += cur_exp_count_diff
                            hyp_exp_counts[b] += cur_exp_count_diff
                            
                            parse_score = score_function((hyp_exp_counts[a], hyp_exp_counts[b]))
                            parses_with_scores[exp].append(((a,b), parse_score))
                            parse_scores.append((parse_score, (a, b), hyp_exp_counts, cur_exp_count_diff))
                        
                        selected_parse_score, selected_parse, exp_counts, cur_exp_count_diff = max(parse_scores)
                        selected_parses[exp] = selected_parse, selected_parse_score, cur_exp_count_diff
                
                ### IF ADDING NEW AFFIXES ###
                # if ADD_NEW_AFFIXES:
                #     # if exp starts or ends with token_a 
                #     if not parsed_with_token_b:
                #         if exp.startswith(token_a):
                #             pot_new_exp = exp.split(token_a)[-1].strip()
                #             if len(pot_new_exp) == 0: continue
                #             if pot_new_exp in selected_parses: continue
                #             if pot_new_exp not in potential_new_exps_endswith:
                #                 potential_new_exps_endswith[pot_new_exp] = [] # list of exps that contain the potential new exp
                #             potential_new_exps_endswith[pot_new_exp].append(exp)

                #         if exp.endswith(token_a):
                #             pot_new_exp = exp.split(token_a)[0].strip()
                #             if len(pot_new_exp) == 0: continue
                #             if pot_new_exp in selected_parses: continue
                #             if pot_new_exp not in potential_new_exps_startswith:
                #                 potential_new_exps_startswith[pot_new_exp] = [] # list of exps that contain the potential new exp
                #             potential_new_exps_startswith[pot_new_exp].append(exp)
                ####################################################################
        
            if not was_parsed:
                default_score = score_function((exp_counts[default_parse[0]], exp_counts[default_parse[1]]))
                selected_parses[exp] = default_parse, default_score, "NO PARSING AVAILABLE"
                parses_with_scores[exp].append((default_parse, default_score))

            if i == STOP:
                break

        
        ######## IF ADDING NEW AFFIXES BASED ON REOCCURING SUBSTRINGS ATTACHED TO KNOWN AFFIXES ############
        # if ADD_NEW_AFFIXES:
        #     new_exp_parses = {}
        #     for new_exp, exps_that_startwith_new_exp in potential_new_exps_startswith.items():
        #         exps_that_endwith_new_exp = potential_new_exps_endswith.get(new_exp, [])
        #         exps_that_new_exp_attach_to = exps_that_startwith_new_exp + exps_that_endwith_new_exp
        #         # to add to vocab, the new exponent must attach to more than one of the old exponents
        #         if len(exps_that_new_exp_attach_to) > 1:
        #             if new_exp not in exp_counts:
        #                 exp_counts[new_exp] = 0
        #             for exp in exps_that_startwith_new_exp:
        #                 ending_exp = exp.split(new_exp)[-1].strip()
        #                 if ending_exp not in exp_counts:
        #                     exp_counts[ending_exp] = 0
        #                 # update counts
        #                 exp_counts[ending_exp] += exp_counts[exp]
        #                 exp_counts[new_exp] += exp_counts[exp]
        #                 # set new parse for the exponent
        #                 if exp not in new_exp_parses:
        #                     new_exp_parses[exp] = []
        #                 new_exp_parses[exp].append((new_exp, ending_exp))
                        
        #     for new_exp, exps_that_endwith_new_exp in potential_new_exps_endswith.items():
        #         exps_that_startwith_new_exp = potential_new_exps_startswith.get(new_exp, [])
        #         exps_that_new_exp_attach_to = exps_that_endwith_new_exp + exps_that_startwith_new_exp
        #         # to add to vocab, the new exponent must attach to more than one of the old exponents
        #         if len(exps_that_new_exp_attach_to) > 1:
        #             if new_exp not in exp_counts:
        #                 exp_counts[new_exp] = 0
        #             for exp in exps_that_endwith_new_exp:
        #                 starting_exp = exp.split(new_exp)[0].strip()
        #                 if starting_exp not in exp_counts:
        #                     exp_counts[starting_exp] = 0
        #                 # update counts
        #                 exp_counts[starting_exp] += exp_counts[exp]
        #                 exp_counts[new_exp] += exp_counts[exp]
        #                 # set new parse for the exponent
        #                 if exp not in new_exp_parses:
        #                     new_exp_parses[exp] = []
        #                 new_exp_parses[exp].append((starting_exp, new_exp))

        #     for exp, new_parses in new_exp_parses.items():
        #         exp_new_parse_scores = [
        #             (score_function((exp_counts[a], exp_counts[b])), (a,b))
        #             for a, b in new_parses
        #         ]
        #         for parse, parse_score in parses_with_scores[exp]:
        #             exp_new_parse_scores.append((parse_score, parse))

        #         exp_new_parse_scores.sort(reverse=True)
        #         parses_with_scores[exp] = [
        #             (parse, parse_score) 
        #             for parse_score, parse in exp_new_parse_scores
        #         ]
        #         selected_parse_score, selected_parse = exp_new_parse_scores[0]
        #         selected_parses[exp] = selected_parse, selected_parse_score, "FOUND NEW PARSE"
        ######################################################################################

        if STOP:
            out_file = csv_file.replace(".csv", f".{score}.iter-{iteration}.splits.subsets.{STOP}.csv")
        else:
            out_file = csv_file.replace(".csv", f".{score}.iter-{iteration}.splits.subsets.csv")
        if ADD_NEW_AFFIXES:
            out_file = out_file.replace(".csv", ".NEW_AFFIXES.csv")

        out_dir = out_file.split(".csv")[0].replace(f".iter-{iteration}", "")
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        out_file_name = out_file.split("/")[-1]
        out_file = os.path.join(out_dir, out_file_name)
        # out_model_file = out_file.replace(".csv", ".model.csv")

        with open(out_file, "w") as outf:
            #, open(out_model_file, "w") as modelf:
            # model_writer = csv.writer(modelf)
            for exp, (parse, parse_score, other) in selected_parses.items():
                outf.write("\n" + exp + "\n")
                outf.write(f"\tSELECTED: {str(parse)}, score: {parse_score}, other:{other}\n")
                outf.write("\tOTHER:\n")
                for other_parse, other_parse_score in parses_with_scores[exp]:
                    if other_parse == parse: continue
                    outf.write(f"\t\t{str(other_parse)}, score: {other_parse_score}\n")
                # model_writer.writerow([parse, parse_score])

        last_iteration_exponents = set([exp for _, exp in data])
        exponents_for_next_iter = set()
        for exp, (parse, _, _) in selected_parses.items():
            a, b = parse
            # print(a, b)
            if a:
                exponents_for_next_iter.add(a)
            if b:
                exponents_for_next_iter.add(b)
        # if no change in vocab, break the loop
        if last_iteration_exponents == exponents_for_next_iter:
            break
        data = [(exp_counts[exp], exp) 
                for exp in exponents_for_next_iter]
        data.sort(reverse=True)

    ######## IF ADDING NEW AFFIXES BASED ON REOCCURING SUBSTRINGS ATTACHED TO KNOWN AFFIXES ############
    if ADD_NEW_AFFIXES:
        print("LOOKING FOR NEW AFFIXES")
        potential_new_exps_startswith = {}
        potential_new_exps_endswith = {}
        visited = []
        exp_counts = {exp: count for count, exp in data}
        exp_counts.update({None: 0})
        total = len(data)
        if STOP:
            total=STOP

        for i, (_, exp) in tqdm(enumerate(data), total=total):
            visited.append(exp)
            default_parse = (exp, None)
            parses[exp] = [default_parse]
            parses_with_scores[exp] = []
            was_parsed = False
            for token_a in visited:
                # if exp starts or ends with token_a 
                if exp.startswith(token_a):
                    pot_new_exp = exp.split(token_a)[-1].strip()
                    if len(pot_new_exp) == 0: continue
                    if pot_new_exp in selected_parses: continue
                    if pot_new_exp not in potential_new_exps_endswith:
                        potential_new_exps_endswith[pot_new_exp] = [] # list of exps that contain the potential new exp
                    potential_new_exps_endswith[pot_new_exp].append(exp)

                if exp.endswith(token_a):
                    pot_new_exp = exp.split(token_a)[0].strip()
                    if len(pot_new_exp) == 0: continue
                    if pot_new_exp in selected_parses: continue
                    if pot_new_exp not in potential_new_exps_startswith:
                        potential_new_exps_startswith[pot_new_exp] = [] # list of exps that contain the potential new exp
                    potential_new_exps_startswith[pot_new_exp].append(exp)

        new_exp_parses = {}
        for new_exp, exps_that_startwith_new_exp in potential_new_exps_startswith.items():
            exps_that_endwith_new_exp = potential_new_exps_endswith.get(new_exp, [])
            exps_that_new_exp_attach_to = exps_that_startwith_new_exp + exps_that_endwith_new_exp
            # to add to vocab, the new exponent must attach to more than one of the old exponents
            if len(exps_that_new_exp_attach_to) > 1:
                if new_exp not in exp_counts:
                    exp_counts[new_exp] = 0
                for exp in exps_that_startwith_new_exp:
                    ending_exp = exp.split(new_exp)[-1].strip()
                    if ending_exp not in exp_counts:
                        exp_counts[ending_exp] = 0
                    # update counts
                    exp_counts[ending_exp] += exp_counts[exp]
                    exp_counts[new_exp] += exp_counts[exp]
                    # set new parse for the exponent
                    if exp not in new_exp_parses:
                        new_exp_parses[exp] = []
                    new_exp_parses[exp].append((new_exp, ending_exp))
                    
        for new_exp, exps_that_endwith_new_exp in potential_new_exps_endswith.items():
            exps_that_startwith_new_exp = potential_new_exps_startswith.get(new_exp, [])
            exps_that_new_exp_attach_to = exps_that_endwith_new_exp + exps_that_startwith_new_exp
            # to add to vocab, the new exponent must attach to more than one of the old exponents
            if len(exps_that_new_exp_attach_to) > 1:
                if new_exp not in exp_counts:
                    exp_counts[new_exp] = 0
                for exp in exps_that_endwith_new_exp:
                    starting_exp = exp.split(new_exp)[0].strip()
                    if starting_exp not in exp_counts:
                        exp_counts[starting_exp] = 0
                    # update counts
                    exp_counts[starting_exp] += exp_counts[exp]
                    exp_counts[new_exp] += exp_counts[exp]
                    # set new parse for the exponent
                    if exp not in new_exp_parses:
                        new_exp_parses[exp] = []
                    new_exp_parses[exp].append((starting_exp, new_exp))

        for exp, new_parses in new_exp_parses.items():
            exp_new_parse_scores = [
                (score_function((exp_counts[a], exp_counts[b])), (a,b))
                for a, b in new_parses
            ]
            for parse, parse_score in parses_with_scores[exp]:
                exp_new_parse_scores.append((parse_score, parse))

            exp_new_parse_scores.sort(reverse=True)
            parses_with_scores[exp] = [
                (parse, parse_score) 
                for parse_score, parse in exp_new_parse_scores
            ]
            selected_parse_score, selected_parse = exp_new_parse_scores[0]
            selected_parses[exp] = selected_parse, selected_parse_score, "FOUND NEW PARSE"

        out_file = out_file.replace(f"iter-{iteration}", "NEW_AFFIXES")
        with open(out_file, "w") as outf:
            for exp, (parse, parse_score, other) in selected_parses.items():
                outf.write("\n" + exp + "\n")
                outf.write(f"\tSELECTED: {str(parse)}, score: {parse_score}, other:{other}\n")
                outf.write("\tOTHER:\n")
                for other_parse, other_parse_score in parses_with_scores[exp]:
                    if other_parse == parse: continue
                    outf.write(f"\t\t{str(other_parse)}, score: {other_parse_score}\n")

        exponents_for_final_iter = set()
        for exp, (parse, _, _) in selected_parses.items():
            a, b = parse
            # print(a, b)
            if a:
                exponents_for_final_iter.add(a)
            if b:
                exponents_for_final_iter.add(b)
        data = [(exp_counts[exp], exp) 
                for exp in exponents_for_next_iter]
        data.sort(reverse=True)

    # TODO check that final vocab accounts for all vocab?
    if STOP:
        model_file = csv_file.replace(".csv", f".{score}.{STOP}.model.csv")
    else:
        model_file = csv_file.replace(".csv", f".{score}.{STOP}.model.csv")  
    if ADD_NEW_AFFIXES:
        model_file = model_file.replace(".model.csv", ".NEW_AFFIXES.model.csv")
    with open(model_file, "w", newline="") as outf:
        writer = csv.writer(outf)
        for count, exp in data:
            exp = exp.replace(" ", "").strip()
            writer.writerow([exp, count])


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="/home/hatch5o6/LING590R/code/aligned_families/rm_ws_celex.removed.suffix.raw.csv")
    parser.add_argument("--STOP", type=int, default=None)
    parser.add_argument("--score", default="max", choices=["max", "sum"])
    parser.add_argument("--ADD_NEW_AFFIXES", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    # if args.score == "max":
    #     score = max
    # elif args.score == "sum":
    #     score = sum
    run(args.csv, STOP=args.STOP, ADD_NEW_AFFIXES=args.ADD_NEW_AFFIXES, score=args.score)
