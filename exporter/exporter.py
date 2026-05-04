import psycopg2
import pandas as pd
from minio import Minio
from datetime import datetime
import json
import os

STATE_FILE = "exporter/state.json"

# --- читаем state ---
last_id = 0

if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            last_id = state.get("last_payment_id", 0)
    except:
        print("State file empty or corrupted, starting from 0")

print(f"Last processed id: {last_id}")

# --- подключение к postgres ---
conn = psycopg2.connect(
    host="localhost",
    database="fintech_db",
    user="admin",
    password="admin123"
)

# --- запрос только новых данных ---
query = f"""
SELECT * FROM payments
WHERE payment_id > {last_id}
ORDER BY payment_id;
"""

df = pd.read_sql(query, conn)

# --- если нет новых данных ---
if df.empty:
    print("No new data")
    exit()

# --- создаем файл ---
file_name = f"payments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
df.to_parquet(file_name, index=False)

print(f"Saved locally: {file_name}")

# --- подключение к MinIO ---
client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="admin123",
    secure=False
)

bucket_name = "bronze"

# --- partitioning по дате ---
date_part = datetime.now().strftime("%Y-%m-%d")

object_name = f"payments/{date_part}/{file_name}"

# --- загрузка в MinIO ---
client.fput_object(
    bucket_name,
    object_name,
    file_name
)

print(f"Uploaded to MinIO: {object_name}")

# --- удаляем локальный файл ---
os.remove(file_name)
print(f"Deleted local file: {file_name}")

# --- обновляем state ---
new_last_id = int(df["payment_id"].max())

with open(STATE_FILE, "w") as f:
    json.dump({"last_payment_id": new_last_id}, f)

print(f"Updated last_id to: {new_last_id}")