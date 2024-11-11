#!/bin/bash

#SBATCH --time=72:00:00   # walltime.  hours:minutes:seconds
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --gpus=0
#SBATCH --cpus-per-task=24
#SBATCH --mem-per-cpu=5000M   # 5G memory per CPU core
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-user thebrendanhatch@gmail.com
#SBATCH --output /home/hatch5o6/LING590R/code/slurm_outputs/morphalign_celex_removed.out
#SBATCH --job-name=morphalign_celex_removed


morphalign -f sounds_files/celex.csv --cpu 24  -s simple word_families/celex.removed.csv aligned_families/celex.removed.csv
