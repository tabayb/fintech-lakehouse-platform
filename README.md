# Fintech Lakehouse Platform

End-to-end local data engineering project simulating fintech payment pipelines using a lakehouse architecture.

---

## 📌 Overview

This project implements a full data pipeline:

PostgreSQL → Bronze (MinIO) → Silver (Clean Layer)

---

## ⚙️ Architecture

```text
Python Generator
        ↓
PostgreSQL (OLTP source)
        ↓
Exporter (Incremental Load)
        ↓
MinIO (Bronze Layer - Raw Data)
        ↓
Transform (Cleaning)
        ↓
MinIO (Silver Layer - Clean Data)
```

---

## 🚀 Features

### Data Ingestion

* Incremental loading (no full reloads)
* Watermark tracking via `state.json`
* Idempotent pipeline behavior

### Data Storage

* MinIO (S3-compatible storage)
* Partitioned data by date
* Parquet format (columnar, compressed)

### Data Transformation

* Deduplication
* Data validation (e.g. amount > 0)
* Standardization (currency, status)

---

## 🗂️ Data Layout

### Bronze (Raw)

```
bronze/payments/YYYY-MM-DD/*.parquet
```

### Silver (Clean)

```
silver/payments/YYYY-MM-DD/*.parquet
```

---

## 🧱 Tech Stack

* Python
* Docker
* PostgreSQL
* MinIO (S3)

---

## ▶️ How to Run

### 1. Start services

```
docker compose up -d
```

### 2. Generate data

```
python generator/generator.py
```

### 3. Run ingestion (Bronze)

```
python exporter/exporter.py
```

### 4. Run transformation (Silver)

```
python silver/transform.py
```

---

## 🧠 Concepts Covered

* Data Lake vs OLTP
* Incremental vs Full Load
* Watermarks & State Management
* Partitioning
* Parquet format
* Bronze / Silver architecture

---

## 📈 Status

V1 (Bronze + Incremental + Parquet + Partitioning) ✅
V2 (Silver Layer - Data Cleaning) 🚧

---

## 🛣️ Roadmap

* Kafka (streaming ingestion)
* Spark (distributed processing)
* dbt (transformations)
* Airflow (orchestration)
* Gold layer (analytics)

---
