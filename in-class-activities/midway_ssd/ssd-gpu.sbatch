#!/bin/bash

#SBATCH --job-name=ssd-gpu-example
#SBATCH --output=ssd-gpu.out
#SBATCH --error=ssd-gpu.err
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --partition=ssd-gpu
#SBATCH --account=ssd
#SBATCH --qos=ssd

module load python/anaconda-2022.05 cuda/11.7

python cupy_rand_walk.py