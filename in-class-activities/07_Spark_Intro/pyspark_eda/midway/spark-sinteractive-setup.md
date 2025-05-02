# Running Interactive Spark Jobs on Midway 3

In order to run PySpark code in an interactive Jupyter notebook on Midway 3, we need to do the following:

First, we will need to set up our environment on Midway 3 such that typing pyspark will automatically launch a Jupyter Lab server for us. Specifically, we should edit our `.bashrc` file from a Midway 3 login node using nano:

```bash
nano ~/.bashrc
```

Once the nano editor has opened, add the following lines to the bottom of your `.bashrc` file to configure PySpark to work with the version of Anaconda we've been using in the class, and also configure `pyspark` to launch a Jupyter Lab server automatically. Note that we are echo-ing the Host IP address so that we can use this information for port forwarding to our local machine later on.

```bash
export PYSPARK_PYTHON=/software/python-anaconda-2022.05-el8-x86_64/bin/python3
export PYSPARK_DRIVER_PYTHON="jupyter"

# Display Host IP at start of each session so can copy for interactive sessions
HOST_IP=`/sbin/ip route get 8.8.8.8 | awk '{print $7;exit}'`
echo $HOST_IP
export PYSPARK_DRIVER_PYTHON_OPTS="lab --no-browser --ip=$HOST_IP --port=8888"
export XDG_RUNTIME_DIR=''
```

Save and exit your .bashrc file. Then, run:

```bash
source ~/.bashrc
```

After you've done this once, you no longer need to perform this step again. Your environment is ready to go!

---

To run a PySpark notebook in interactive mode, enter into an sinteractive session (using relevant sbatch commands; here, requesting the same resources as in the `spark.sbatch` script in this directory for one hour):

```bash
sinteractive --time=01:00:00 --nodes=1 --ntasks=10 --mem=40G --partition=caslake --account=macs30113
```

Once you have entered into the interactive session, you will see your host IP printed above the command prompt (this is what we requested to happen when your `~/.bashrc` file is loaded). This should be a series of numbers and periods that looks like `10.50.250.12` (or any other series of numbers). Copy this IP address so that we can use it to for port forwarding below.

Then load your modules and launch your PySpark Jupyter server with the same parameters provided to `spark-submit` in a sbatch script (here, the same as `spark.sbatch`):

```bash
module load python/anaconda-2022.05 spark/3.3.2
pyspark --total-executor-cores 9 --executor-memory 4G --driver-memory 4G
```

In a local terminal window, [follow the RCC instructions](https://rcc-uchicago.github.io/user-guide/software/apps-and-envs/python/#running-jupyter-notebooks) to forward the port of your remote Jupyter Server to your local port (step 4). For instance, given the above setup, if the host IP that you copied was `10.50.250.12`, you would run the following in your local terminal to forward to your local machine:

```bash
ssh -NL 8888:10.50.250.12:8888 <your-CNetID>@midway3.rcc.uchicago.edu
```

Note that once you log in, nothing will appear on your screen (this is expected given the -N flag). As long as you keep this local terminal window open, your remote content on port 8888 will be forwarded to your local port 8888. After logging in, you will be able to open the Jupyter Server URL `http://127.0.0.1:8888/?token=....` (printed out when you launched the server in your remote terminal window), or equivalently, `localhost:8888/?token=....` in the browser on your local machine.

You should now be able to run `spark-midway.ipynb` (included in this directory), or any PySpark Jupyter notebook in this Jupyter Lab environment.