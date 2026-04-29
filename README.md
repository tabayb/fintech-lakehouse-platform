# Fintech Lakehouse Platform

End-to-end local data engineering project simulating fintech payment pipelines using lakehouse architecture.

## Project Goal

Build a modern local data platform to learn and practice:

* Docker
* PostgreSQL
* MinIO
* Python data generation
* EL / ELT pipelines
* Bronze / Silver / Gold architecture
* Future: Kafka, Spark, dbt, Airflow

## Architecture (V1)

```text
Python Payment Generator
        ↓
PostgreSQL (source system)
        ↓
Export Raw Events
        ↓
MinIO (Bronze Layer)
```

## Source Tables

### payments

Stores current payment state.

### payment_events

Stores historical lifecycle events for each payment.

## Event Types

* payment_initiated
* payment_authorized
* payment_completed
* payment_failed
* payment_refunded
* payment_chargeback
* payment_cancelled

## Tech Stack

* Python
* Docker
* PostgreSQL
* MinIO

## Roadmap

### V1

* Local source system
* Payment generator
* Export raw data to MinIO

### V2

* Kafka streaming ingestion

### V3

* Spark transformations

### V4

* dbt models

### V5

* Airflow orchestration

## Status

Planning / Initial Setup
