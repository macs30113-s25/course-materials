#!/bin/bash

#SBATCH --job-name=spark-nlp-example
#SBATCH --output=spark-nlp.out
#SBATCH --error=spark-nlp.err
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=40G
#SBATCH --partition=caslake
#SBATCH --account=macs30113

module load python/anaconda-2022.05 spark/3.3.2

export PYSPARK_DRIVER_PYTHON=/software/python-anaconda-2022.05-el8-x86_64/bin/python3
export PYSPARK_PYTHON=/software/python-anaconda-2022.05-el8-x86_64/bin/python3

spark-submit --total-executor-cores 9 --executor-memory 4G --driver-memory 4G --jars /project/macs30113/spark-jars/spark-nlp_2.12-3.3.2.jar spark_nlp.py

# to filter out logging messages from output, run the following:
# cat spark-nlp.out | grep -vE "INFO|WARN|rdd|UserWarning"