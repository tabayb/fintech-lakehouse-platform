from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    current_date,
    lit,
    monotonically_increasing_id
)

spark = (
    SparkSession.builder
    .appName("BuildDimCustomerSCD2")
    .getOrCreate()
)

df = spark.read.parquet(
    "gold/dim_customer"
)

dim_customer_scd2 = (
    df
    .withColumn(
        "customer_sk",
        monotonically_increasing_id() + 1
    )
    .withColumn(
        "effective_date",
        current_date()
    )
    .withColumn(
        "end_date",
        lit(None).cast("date")
    )
    .withColumn(
        "is_current",
        lit("Y")
    )
)

dim_customer_scd2 = dim_customer_scd2.select(
    "customer_sk",
    "customer_id",
    "customer_name",
    "customer_country",
    "segment",
    "signup_date",
    "effective_date",
    "end_date",
    "is_current"
)

print("\nDIM CUSTOMER SCD2")

dim_customer_scd2.show(10, truncate=False)

dim_customer_scd2.write \
    .mode("overwrite") \
    .parquet(
        "gold/dim_customer_scd2"
    )

spark.stop()