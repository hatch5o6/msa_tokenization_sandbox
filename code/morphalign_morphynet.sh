#!/bin/bash

#SBATCH --time=72:00:00   # walltime.  hours:minutes:seconds
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --gpus=0
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=5000M   # 5G memory per CPU core
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-user thebrendanhatch@gmail.com
#SBATCH --output /home/hatch5o6/LING590R/code/slurm_outputs/morphalign_morphynet.out
#SBATCH --job-name=morphalign_morphynet


morphalign -f sounds_files/morphynet.csv --cpu 16  -s simple word_families/morphynet.csv aligned_families/morphynet.csv
