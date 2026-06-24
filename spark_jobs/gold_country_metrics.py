from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    count,
    sum,
    avg
)

spark = (
    SparkSession.builder
    .appName("CountryMetrics")
    .getOrCreate()
)

df = spark.read.parquet(
    "silver/payment_enriched"
)

payments_only_df = (
    df
    .dropDuplicates(["payment_id"])
)

gold_df = (
    payments_only_df
    .groupBy("customer_country")
    .agg(
        count("*").alias("payments_count"),
        sum("amount").alias("total_amount"),
        avg("amount").alias("avg_amount")
    )
    .orderBy("payments_count", ascending=False)
)

print("\nCOUNTRY METRICS")

gold_df.show(truncate=False)

print("\nPHYSICAL PLAN")

gold_df.explain("formatted")

gold_df.write \
    .mode("overwrite") \
    .parquet(
        "gold/country_metrics"
    )

print("\nGold country_metrics saved")

spark.stop()