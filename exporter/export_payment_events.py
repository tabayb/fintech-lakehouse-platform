import pandas as pd
import psycopg2
from minio import Minio
from datetime import datetime
import os

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="fintech_db",
    user="admin",
    password="admin123"
)

query = """
SELECT *
FROM payment_events;
"""

df = pd.read_sql(query, conn)

if df.empty:
    print("No payment events found")
    exit()

# Create parquet file
file_name = f"payment_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"

df.to_parquet(file_name, index=False)

print(f"Saved locally: {file_name}")

# MinIO connection
client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="admin123",
    secure=False
)

bucket_name = "bronze"

date_part = datetime.now().strftime("%Y-%m-%d")

object_name = f"payment_events/{date_part}/{file_name}"

# Upload to MinIO
client.fput_object(
    bucket_name,
    object_name,
    file_name
)

print(f"Uploaded to MinIO: {object_name}")

# Remove local parquet
os.remove(file_name)

print(f"Deleted local file: {file_name}")

conn.close()

print("Payment events exported successfully")