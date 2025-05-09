#!/bin/bash

#SBATCH --job-name=graphframes-example
#SBATCH --output=graphframes.out
#SBATCH --error=graphframes.err
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=40G
#SBATCH --partition=caslake
#SBATCH --account=macs30113

module load python/anaconda-2022.05 spark/3.3.2

export PYSPARK_DRIVER_PYTHON=/software/python-anaconda-2022.05-el8-x86_64/bin/python3
export PYSPARK_PYTHON=/software/python-anaconda-2022.05-el8-x86_64/bin/python3

spark-submit --total-executor-cores 9 --executor-memory 4G --driver-memory 4G --jars /project/macs30113/spark-jars/graphframes-0.8.3-spark3.4-s_2.12.jar pagerank.py

# to filter out logging messages from output, run the following:
# cat graphframes.out | grep -vE "INFO|WARN|rdd|UserWarning"