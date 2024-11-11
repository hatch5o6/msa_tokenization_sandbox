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
#SBATCH --output /home/hatch5o6/LING590R/code/slurm_outputs/label_words.out
#SBATCH --job-name=label_words
#SBATCH --qos=dw87

python label_words.py \
    -w data/ccmatrix_en_words.20k.txt \
    -o root_labels/ccmatrix_en_words.20k.labels.txt \
    --LIMIT 1000
