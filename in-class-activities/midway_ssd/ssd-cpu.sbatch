#!/bin/bash

#SBATCH --job-name=ssd-cpu-example
#SBATCH --output=ssd-cpu.out
#SBATCH --error=ssd-cpu.err
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --partition=ssd
#SBATCH --account=ssd

module load python/anaconda-2022.05 mpich/3.2.1

mpirun python mpi_rand_walk.py