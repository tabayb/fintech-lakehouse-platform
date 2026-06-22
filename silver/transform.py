from pyspark.sql import SparkSession

spark = (
SparkSession.builder
.appName("BronzeToSilver")
.getOrCreate()
)

df = spark.read.parquet("bronze/payments/*/*.parquet")

print("Rows:", df.count())

df.printSchema()

df.show(5, truncate=False)

spark.stop()
