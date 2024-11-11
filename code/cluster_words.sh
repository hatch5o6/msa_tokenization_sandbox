#!/bin/bash

#SBATCH --time=24:00:00   # walltime.  hours:minutes:seconds
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --gpus=1
#SBATCH --mem-per-cpu=64000M   # 64G memory per CPU core
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-user thebrendanhatch@gmail.com
#SBATCH --output /home/hatch5o6/LING590R/code/slurm_outputs/cluster_words.out
#SBATCH --job-name=cluster_words
#SBATCH --qos=dw87

python cluster_words.py \
    -w data/ccmatrix_en_words.20k.txt \
    -o word_families/ccmatrix_en_words.20k.fam.txt \
    --LIMIT 1000
