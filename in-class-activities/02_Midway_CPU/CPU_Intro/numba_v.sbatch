#!/bin/bash

#SBATCH --job-name=numba_v
#SBATCH --output=numba_v.out
#SBATCH --error=numba_v.err
#SBATCH --account=macs30113
#SBATCH --partition=caslake
#SBATCH --ntasks=1

# Load Python module
module load python/anaconda-2022.05

# Compile Vectorized Numba function and compare performance to regular NumPy
python ./distance_functions.py
