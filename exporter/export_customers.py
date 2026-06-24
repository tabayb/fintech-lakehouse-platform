import pandas as pd
import psycopg2
from minio import Minio
from datetime import datetime
import os

conn = psycopg2.connect(
    host="localhost",
    database="fintech_db",
    user="admin",
    password="admin123"
)

query = """
SELECT *
FROM customers;
"""

df = pd.read_sql(query, conn)

file_name = f"customers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"

df.to_parquet(file_name, index=False)

client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="admin123",
    secure=False
)

bucket_name = "bronze"

date_part = datetime.now().strftime("%Y-%m-%d")

object_name = f"customers/{date_part}/{file_name}"

client.fput_object(
    bucket_name,
    object_name,
    file_name
)

os.remove(file_name)

print("Customers exported")