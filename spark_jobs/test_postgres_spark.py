from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("PostgresSparkTest")
    .config(
        "spark.jars",
        "jars/postgresql-42.7.7.jar"
    )
    .getOrCreate()
)

df = (
    spark.read
    .format("jdbc")
    .option("url", "jdbc:postgresql://localhost:5432/fintech_db")
    .option("dbtable", "payments")
    .option("user", "admin")
    .option("password", "admin123")
    .option("driver", "org.postgresql.Driver")
    .load()
)

print("Rows:", df.count())

df.show(5, truncate=False)

spark.stop()