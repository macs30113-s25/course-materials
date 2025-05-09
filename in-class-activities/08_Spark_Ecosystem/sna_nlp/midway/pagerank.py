from pyspark.sql import SparkSession
from graphframes import GraphFrame

spark = SparkSession \
        .builder \
        .appName('graphframes') \
        .getOrCreate()

# load data
vertices = spark.read.csv('/project/macs30113/comic/nodes.csv', header=True)
edges = spark.read.csv('/project/macs30113/comic/edges.csv', header=True)

# Create graph
vertices = vertices.withColumnRenamed('node', 'id')
edges = (edges.withColumnRenamed('comic', 'src')
              .withColumnRenamed('hero', 'dst')
        )
g = GraphFrame(vertices, edges)

# Run PageRank algorithm as a weighted measure of popularity and show results
results = g.pageRank(resetProbability=0.01, maxIter=20)
results.vertices.select('id', 'pagerank').sort('pagerank', ascending=False).show()