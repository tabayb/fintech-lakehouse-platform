from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("FintechLakehouse")
    .master("local[*]")
    .getOrCreate()
)

print("Spark started successfully")

data = [
    (1, "Abay"),
    (2, "John")
]

df = spark.createDataFrame(data, ["id", "name"])

df.show()

spark.stop()