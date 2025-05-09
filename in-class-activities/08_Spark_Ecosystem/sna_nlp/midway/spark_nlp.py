import sparknlp
import pyspark.sql.functions as F
from sparknlp.annotator import Tokenizer, PerceptronModel
from sparknlp.base import DocumentAssembler
from pyspark.ml import Pipeline

spark = sparknlp.start()

sample = [
    [0, 'The University of Chicago was incorporated as a coeducational institution in 1890 by the American Baptist Education Society, using $400,000 donated to the ABES to match a $600,000 donation from Baptist oil magnate and philanthropist John D. Rockefeller, and including land donated by Marshall Field. While the Rockefeller donation provided money for academic operations and long-term endowment, it was stipulated that such money could not be used for buildings. The Hyde Park campus was financed by donations from wealthy Chicagoans like Silas B. Cobb who provided the funds for the campus first building, Cobb Lecture Hall, and matched Marshall Fields pledge of $100,000. Other early benefactors included businessmen Charles L. Hutchinson (trustee, treasurer and donor of Hutchinson Commons), Martin A. Ryerson (president of the board of trustees and donor of the Ryerson Physical Laboratory) Adolphus Clay Bartlett and Leon Mandel, who funded the construction of the gymnasium and assembly hall, and George C. Walker of the Walker Museum, a relative of Cobb who encouraged his inaugural donation for facilities.'],
    [1, 'The Hyde Park campus continued the legacy of the original university of the same name, which had closed in the 1880s after its campus was foreclosed on. What became known as the Old University of Chicago had been founded by a small group of Baptist educators in 1856 through a land endowment from Senator Stephen A. Douglas. After a fire, it closed in 1886. Alumni from the Old University of Chicago are recognized as alumni of the present University of Chicago. The university depiction on its coat of arms of a phoenix rising from the ashes is a reference to the fire, foreclosure, and demolition of the Old University of Chicago campus. As an homage to this pre-1890 legacy, a single stone from the rubble of the original Douglas Hall on 34th Place was brought to the current Hyde Park location and set into the wall of the Classics Building. These connections have led the dean of the college and University of Chicago and professor of history John Boyer to conclude that the University of Chicago has, a plausible genealogy as a pre–Civil War institution']
]

data = spark.createDataFrame(sample) \
            .toDF("id", "text")

documentAssembler = DocumentAssembler()\
    .setInputCol("text")\
    .setOutputCol("document")

tokenizer = Tokenizer() \
    .setInputCols(["document"]) \
    .setOutputCol("token")

# instead of using pretrained for online:
#pos = PerceptronModel.pretrained("pos_anc", 'en')\
#        .setInputCols("document", "token")\
#        .setOutputCol("pos")

# download model, extract it, and use .load
pos = PerceptronModel.load("/project/macs30113/spark-jars/pos_anc_en_3.0.0_3.0_1614962126490/")\
      .setInputCols("document", "token")\
      .setOutputCol("pos")

my_pipeline = Pipeline(
      stages = [
          documentAssembler,
          tokenizer,
          pos
      ])

pipelineModel = my_pipeline.fit(data)

# transform data
result = pipelineModel.transform(data)


# Display part of speech for first 20 tokens
pos_df = result.select('id', F.explode(F.arrays_zip('token.result',
                                                    'pos.result',
                                          )).alias('pos'))
pos_df.show(truncate=False)