import random
from datetime import date, timedelta

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="fintech_db",
    user="admin",
    password="admin123"
)

cur = conn.cursor()

countries = ["US", "KZ", "DE"]
segments = ["Retail", "Premium", "Corporate"]

for customer_id in range(1, 101):

    customer_name = f"Customer_{customer_id}"

    country = random.choice(countries)

    segment = random.choice(segments)

    signup_date = date.today() - timedelta(
        days=random.randint(1, 1000)
    )

    cur.execute(
        """
        INSERT INTO customers (
            customer_id,
            customer_name,
            country,
            segment,
            signup_date
        )
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT (customer_id)
        DO NOTHING;
        """,
        (
            customer_id,
            customer_name,
            country,
            segment,
            signup_date
        )
    )

conn.commit()

cur.close()
conn.close()

print("Customers loaded")