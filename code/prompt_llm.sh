#!/bin/bash

#SBATCH --time=48:00:00   # walltime.  hours:minutes:seconds
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --gpus=1
#SBATCH --mem-per-cpu=64000M   # 64G memory per CPU core
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-user thebrendanhatch@gmail.com
#SBATCH --output /home/hatch5o6/LING590R/code/slurm_outputs/prompt_llm.out
#SBATCH --job-name=prompt_llm
#SBATCH --qos=dw87

nvidia-smi
python cluster_words.py \
    --words \
    --model /home/hatch5o6/nobackup/archive/huggingface/models/Meta-Llama-3-8B \
    --LIMIT 100 \
    --out results/100_words.txt