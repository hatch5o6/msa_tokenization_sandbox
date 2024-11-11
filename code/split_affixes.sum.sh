echo "SUFFIXES"
python split_affixes.py \
    --csv /home/hatch5o6/LING590R/code/aligned_families/rm_ws_celex.removed.suffix.raw.csv \
    --STOP 1000 \
    --score sum \

echo "INFIXES"
python split_affixes.py \
    --csv /home/hatch5o6/LING590R/code/aligned_families/rm_ws_celex.removed.infix.raw.csv \
    --STOP 1000 \
    --score sum \
    
echo "PREFIXES"
python split_affixes.py \
    --csv /home/hatch5o6/LING590R/code/aligned_families/rm_ws_celex.removed.prefix.raw.csv \
    --STOP 1000 \
    --score sum \