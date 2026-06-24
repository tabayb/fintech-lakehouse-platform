from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("BronzeToSilver")
    .config(
        "spark.jars",
        "jars/postgresql-42.7.7.jar"
    )
    .getOrCreate()
)

jdbc_url = "jdbc:postgresql://localhost:5432/fintech_db"

properties = {
    "user": "admin",
    "password": "admin123",
    "driver": "org.postgresql.Driver"
}

# customers
customers_df = (
    spark.read.jdbc(
        url=jdbc_url,
        table="customers",
        properties=properties
    )
)

customers_df = (
    customers_df
    .withColumnRenamed(
        "country",
        "customer_country"
    )
)

# payments
payments_df = (
    spark.read.jdbc(
        url=jdbc_url,
        table="payments",
        properties=properties
    )
)

# payment_events
events_df = (
    spark.read.jdbc(
        url=jdbc_url,
        table="payment_events",
        properties=properties
    )
)

print("\nCUSTOMERS")
customers_df.show(5)

print("\nPAYMENTS")
payments_df.show(5)

print("\nEVENTS")
events_df.show(5)

# JOIN 1
payments_customers_df = (
    payments_df.join(
        customers_df,
        on="customer_id",
        how="left"
    )
)

# JOIN 2
payment_enriched_df = (
    payments_customers_df.join(
        events_df,
        on="payment_id",
        how="left"
    )
)

print("\nENRICHED DATA")

payment_enriched_df.show(
    20,
    truncate=False
)

print("\nROWS:")

print(payment_enriched_df.count())


print("\nPHYSICAL PLAN")

payment_enriched_df.explain("formatted")

payment_enriched_df.write \
    .mode("overwrite") \
    .parquet(
        "silver/payment_enriched"
    )

print("Silver layer saved")


spark.stop()