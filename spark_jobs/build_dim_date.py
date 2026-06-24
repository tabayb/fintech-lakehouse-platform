from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    year,
    month,
    dayofmonth,
    quarter,
    dayofweek,
    to_date
)

spark = (
    SparkSession.builder
    .appName("BuildDimDate")
    .getOrCreate()
)

df = spark.read.parquet(
    "silver/payment_enriched"
)

dim_date = (
    df
    .select(
        to_date("created_at").alias("date")
    )
    .dropDuplicates()
    .withColumn("year", year("date"))
    .withColumn("month", month("date"))
    .withColumn("day", dayofmonth("date"))
    .withColumn("quarter", quarter("date"))
    .withColumn("weekday", dayofweek("date"))
)

print("\nDIM DATE")

dim_date.show(truncate=False)

dim_date.write \
    .mode("overwrite") \
    .parquet(
        "gold/dim_date"
    )

spark.stop()