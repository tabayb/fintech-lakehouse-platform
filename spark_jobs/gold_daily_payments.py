from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    to_date,
    countDistinct,
    sum,
    avg,
    count
)

spark = (
    SparkSession.builder
    .appName("GoldDailyPayments")
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
    .withColumn(
        "payment_date",
        to_date("created_at")
    )
    .groupBy("payment_date")
    .agg(
        count("*").alias("payments_count"),
        sum("amount").alias("total_amount"),
        avg("amount").alias("avg_amount")
    )
)

gold_df.show(truncate=False)

gold_df.explain("formatted")

gold_df.write \
    .mode("overwrite") \
    .parquet(
        "gold/daily_payments"
    )

spark.stop()