import nltk
from tqdm import tqdm

def calc_accuracy(ref_segments, hyp_segments):
    assert len(ref_segments) == len(hyp_segments)
    correct = 0
    pairs = list(zip(ref_segments, hyp_segments))
    for ref_segment, hyp_segment in pairs:
        if ref_segment == hyp_segment:
            correct += 1
    return correct, len(ref_segments), correct / len(ref_segments)

def fit_infix(src_word, parse):
    print("FITTING", src_word, parse)
    morphemes = parse.split("|")
    m_idx = 0
    for m, morph in enumerate(morphemes):
        if "<" in morph:
            assert ">" in morph
            assert "-" in morph
            stem = morph.split("<")[0]
            assert "-" in stem

            # get infixes
            infixes_str = morph[len(stem):]
            assert infixes_str.startswith("<")
            assert infixes_str.endswith(">")
            infixes = []
            infix = ""
            i = 0
            print(f"\tstem '{stem}'")
            print(f"\tinfixes_str '{infixes_str}'")
            starting = True
            while i < len(infixes_str):
                if starting:
                    if infixes_str[i] != "<":
                        print(f"ERROR infixes_str[{i}]=={infixes_str[i]} should be '<'")
                    assert infixes_str[i] == "<"
                    starting = False
                else:
                    if infixes_str[i] == ">":
                        assert infix != ""
                        infixes.append(infix)
                        infix = ""
                        starting = True
                    else:
                        infix += infixes_str[i]
                i += 1
            
            print("\tinfixes", infixes)
            # insert infixes into stem
            stem_pieces = stem.split("-")
            s = 0

            while True:
                p = s - 1
                print(f"----- p({p}) s({s}) -----")
                if s not in [0]:
                    prev = stem_pieces[p]
                    p_idx = 0
                    for stem_piece in stem_pieces[:p]:
                        p_idx += len(stem_piece)
                    cur = stem_pieces[s]
                    print("prev", prev)
                    print("cur", cur)
                    selected_infixes = []
                    FOUND_INFIXES = False

                    # POSSIBLE_INFIXES = []
                    prev_infixes_len = len(infixes)
                    for inf_idx, infix in enumerate(infixes):
                        selected_infixes.append(infix)
                        selected_infixes_str = "".join(selected_infixes)
                        print(f"trying {prev} + {selected_infixes_str} + {cur}")
                        pic = prev + selected_infixes_str + cur
                        compare_to = src_word[m_idx + p_idx:m_idx + p_idx + len(pic)]
                        print(f"comparing to src_word[{m_idx} + {p_idx}:{m_idx} + {p_idx} + {len(pic)}] '{compare_to}'")
                        if pic == compare_to:
                            # POSSIBLE_INFIXES.append((selected_infixes, infixes[len(selected_infixes):]))
                            # remove selected infixes from list of infixes
                            infixes = infixes[len(selected_infixes):]
                            FOUND_INFIXES = True
                            print("\tPASSED!")
                            break
                        else:
                            print("\tFAILED")
                    # if len(POSSIBLE_INFIXES) == 0:
                    if FOUND_INFIXES == False:
                        assert len(infixes) == prev_infixes_len
                        s += 1
                        print(f"s ->", s)
                    else:
                        # for selected_infixes, infixes in POSSIBLE_INFIXES:
                        assert len(infixes) == prev_infixes_len - len(selected_infixes)
                        index_to_insert = s
                        for piece in selected_infixes:
                            stem_pieces.insert(index_to_insert, piece)
                            index_to_insert += 1
                        s = index_to_insert + 1
                        print(f"s ->", s)
                else:
                    s += 1
                    print(f"s ->", s)
                if s >= len(stem_pieces):
                    print(f"s == {s}, breaking")
                    break

            stem = "".join(stem_pieces)
            print("src_word", src_word)
            print("predicted stem", stem_pieces, stem)
            print(f"src_word[{m_idx}:{m_idx + len(stem)}] == {src_word[m_idx:m_idx + len(stem)]}")
            if src_word[m_idx:m_idx + len(stem)] == stem:
                print("INSERTION PASSED!")
                passed = True
            else:
                print(f"INSERTION FAILED :( --> {src_word}:{parse}")
                passed = False
            morphemes[m] = stem
            m_idx += len(stem)
        else:
            m_idx += len(morph)

    print("###################################################")
    return passed, "|".join(morphemes)


def remove_junk(ref_segments, hyp_segments):
    assert len(ref_segments) == len(hyp_segments)
    pairs = list(zip(ref_segments, hyp_segments))
    for ref_segment, hyp_segment in pairs:
        pass

if __name__ == "__main__":
    path = "/home/hatch5o6/LING590R/code/msa_model.morphynet_es.M-100.sum/msa_parses"
    div = "val"
    words_path = path + "/words." + div
    parses_path = path + "/parses." + div

    with open(words_path) as inf:
        words = [line.strip() for line in inf.readlines()]
    with open(parses_path) as inf:
        parses = [line.strip() for line in inf.readlines()]
    pairs = list(zip(words, parses))
    n_passed = 0
    total = 0 
    for src_word, parse in tqdm(pairs):
        if "<" in parse:
            passed, morphemes = fit_infix(src_word, parse)
            if passed:
                n_passed += 1
            total += 1
    print(f"{n_passed} / {total} passed, {round(100 * (n_passed / total), 2)}%")

