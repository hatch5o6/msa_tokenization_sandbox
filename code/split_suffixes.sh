#!/bin/bash

#SBATCH --time=48:00:00   # walltime.  hours:minutes:seconds
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --gpus=0
#SBATCH --mem-per-cpu=1G
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-user thebrendanhatch@gmail.com
#SBATCH --output /home/hatch5o6/LING590R/code/slurm_outputs/split_suffixes.out
#SBATCH --job-name=split_suffixes
#SBATCH --qos=dw87

echo "SUFFIXES"
python split_affixes.py \
    --csv /home/hatch5o6/LING590R/code/aligned_families/rm_ws_celex_word_boundaries/celex.simple.no_word_boundaries.removed.suffix.raw.csv \
    --score max \
