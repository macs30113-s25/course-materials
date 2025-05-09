# Installing and Running External Spark Packages on Midway 3

1. In order to use external Spark packages on Midway 3 in PySpark jobs, we first must install their corresponding Python packages. For example, for Graphframes and Spark-NLP, we would run the following on the login node:

    ```bash
    module load python spark
    pip install --user spark-nlp==5.5.0 graphframes==0.6.0
    ```

2. Then, we must download and reference the Spark package ".jar" files in our `sbatch` scripts. We have already uploaded the jar files for Spark-NLP and GraphFrames to our shared `/project/macs30113/` directory and you can reference these files as we do in the sample `spark_nlp.sbatch` and `graphframes.sbatch` scripts in this directory, adding a `--jars` argument to your `spark-submit` command (or `pyspark` command, if you are running an sinteractive session). For instance, to use Spark NLP in a batch job, you could write something like:

    ```bash
    spark-submit --total-executor-cores 9 --executor-memory 4G --driver-memory 4G --jars /project/macs30113/spark-jars/spark-nlp_2.12-3.3.2.jar spark_nlp.py
    ```

    Or, for an interactive PySpark session:

    ```bash
    pyspark --total-executor-cores 9 --executor-memory 4G --driver-memory 4G --jars /project/macs30113/spark-jars/spark-nlp_2.12-3.3.2.jar
    ```

3. You should then be able to run your PySpark code on Midway 3. Just recall that Midway compute nodes don't have access to the internet, so you will need to follow [the Spark NLP instructions](https://sparknlp.org/docs/en/install#offline) for downloading, extracting and loading any NLP models from [Models Hub](https://sparknlp.org/models) that you use in your pipelines offline. We downloaded the `pos_anc` model files, extracted them, and then added them to our /project/macs30113/ directory as an example (so you can also run the sample code in `spark_nlp.py`). Note the slight code change from our online version:

    ```python
    # downloads model from internet:
    pos = PerceptronModel.pretrained("pos_anc", 'en')\
            .setInputCols("document", "token")\
            .setOutputCol("pos")
    ```

    ...to our offline version that we can use on Midway:
    ```python
    # download model, extract it, and use .load for offline access:
    pos = PerceptronModel.load("/project/macs30113/spark-jars/pos_anc_en_3.0.0_3.0_1614962126490/")\
        .setInputCols("document", "token")\
        .setOutputCol("pos")
    ```