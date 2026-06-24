from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("BuildDimCustomer")
    .getOrCreate()
)

df = spark.read.parquet(
    "silver/payment_enriched"
)

dim_customer = (
    df
    .select(
        "customer_id",
        "customer_name",
        "customer_country",
        "segment",
        "signup_date"
    )
    .dropDuplicates(["customer_id"])
)

print("\nDIM CUSTOMER")

print("\nCUSTOMER 20")

dim_customer.filter(
    dim_customer.customer_id == 20
).show(truncate=False)

dim_customer.write \
    .mode("overwrite") \
    .parquet(
        "gold/dim_customer"
    )

spark.stop()