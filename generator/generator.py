import random
import time
from datetime import datetime
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="fintech_db",
    user="admin",
    password="admin123"
)

cur = conn.cursor()

event_types = [
    "payment_initiated",
    "payment_authorized",
    "payment_completed",
    "payment_failed"
]

while True:
    customer_id = random.randint(1, 100)
    merchant_id = random.randint(100, 200)
    amount = round(random.uniform(10, 500), 2)
    currency = "USD"
    payment_method = random.choice(["card", "apple_pay", "google_pay"])
    country = random.choice(["US", "KZ", "DE"])
    status = "initiated"

    cur.execute("""
        INSERT INTO payments (customer_id, merchant_id, amount, currency, payment_method, country, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING payment_id;
    """, (customer_id, merchant_id, amount, currency, payment_method, country, status))

    payment_id = cur.fetchone()[0]

    # создаем события
    events = random.sample(event_types, k=random.randint(2, 3))

    for event in events:
        cur.execute("""
            INSERT INTO payment_events (payment_id, event_type)
            VALUES (%s, %s);
        """, (payment_id, event))

    conn.commit()

    print(f"Generated payment {payment_id}")

    time.sleep(2)