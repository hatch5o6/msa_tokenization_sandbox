echo "SUFFIXES"
python split_affixes.py \
    --csv /home/hatch5o6/LING590R/code/aligned_families/rm_ws_celex_word_boundaries/celex.simple.no_word_boundaries.removed.suffix.raw.csv \
    --score max \

echo "INFIXES"
python split_affixes.py \
    --csv /home/hatch5o6/LING590R/code/aligned_families/rm_ws_celex_word_boundaries/celex.simple.no_word_boundaries.removed.infix.raw.csv \
    --score max \

echo "PREFIXES"
python split_affixes.py \
    --csv /home/hatch5o6/LING590R/code/aligned_families/rm_ws_celex_word_boundaries/celex.simple.no_word_boundaries.removed.prefix.raw.csv \
    --score max \