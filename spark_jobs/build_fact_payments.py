from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date

spark = (
    SparkSession.builder
    .appName("BuildFactPayments")
    .getOrCreate()
)

df = spark.read.parquet(
    "silver/payment_enriched"
)

fact_payments = (
    df
    .dropDuplicates(["payment_id"])
    .select(
        "payment_id",
        "customer_id",
        to_date("created_at").alias("payment_date"),
        "amount",
        "currency",
        "payment_method"
    )
)

print("\nFACT PAYMENTS")

fact_payments.show(10, truncate=False)

fact_payments.write \
    .mode("overwrite") \
    .parquet(
        "gold/fact_payments"
    )

spark.stop()