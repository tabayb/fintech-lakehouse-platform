from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    count,
    sum,
    avg
)

spark = (
    SparkSession.builder
    .appName("CustomerSegmentMetrics")
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
    .groupBy("segment")
    .agg(
        count("*").alias("payments_count"),
        sum("amount").alias("total_amount"),
        avg("amount").alias("avg_amount")
    )
)

print("\nCUSTOMER SEGMENT METRICS")

gold_df.show(truncate=False)

print("\nPHYSICAL PLAN")

gold_df.explain("formatted")

gold_df.write \
    .mode("overwrite") \
    .parquet(
        "gold/customer_segment_metrics"
    )

print("\nGold customer_segment_metrics saved")

spark.stop()