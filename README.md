# 📊 E-commerce Analytics Data Pipeline (dbt + PostgreSQL)

## 🚀 Project Overview

This project builds a complete analytical data pipeline that:

* Ingests raw data into PostgreSQL
* Transforms data using dbt
* Exposes analytics-ready tables using dimensional modeling (Star Schema)

---

## 🔄 Data Lifecycle (Raw → Transformed → Analytics)

```
CSV Files (Raw Data)
        ↓
PostgreSQL (Raw Tables)
        ↓
dbt Staging Layer (Cleaning)
        ↓
Intermediate Layer (Transformation)
        ↓
Marts Layer (Fact & Dimension Tables)
        ↓
Analytics Queries (Insights)
```

**Explanation:**
Raw data is loaded into PostgreSQL. dbt cleans and transforms it into structured layers and creates analytics-ready tables.

---

## 📐 Data Model Diagram (Star Schema)

```
                dim_customers
                      |
                      |
dim_products ---- fct_orders ---- (Measures: quantity, total_amount)
```

**Fact Table:**

* fct_orders → transactional data

**Dimension Tables:**

* dim_customers
* dim_products

---

## ⭐ Star Schema vs 3NF

| Feature     | Star Schema | 3NF          |
| ----------- | ----------- | ------------ |
| Structure   | Simple      | Complex      |
| Performance | Fast        | Slower       |
| Use Case    | Analytics   | Transactions |

**Why Star Schema?**

* Faster queries
* Easy to understand
* Best for reporting

---

## 🥇 Medallion Architecture Implementation

| Layer  | Folder       | Description               |
| ------ | ------------ | ------------------------- |
| Bronze | staging      | Raw cleaned data          |
| Silver | intermediate | Transformed & joined data |
| Gold   | marts        | Final analytics tables    |

---

## 📂 Project Structure

```
models/
  staging/
  intermediate/
  marts/

macros/
tests/
seeds/
```

---

## ⚙️ Setup & Run Instructions

### 1. Start Database

```bash
docker-compose up -d
```

### 2. Load Data

```bash
python ingest_data.py
```

### 3. Check dbt Connection

```bash
dbt debug
```

### 4. Run Models

```bash
dbt run
```

### 5. Run Tests

```bash
dbt test
```

### 6. Check Data Freshness

```bash
dbt source freshness
```

### 7. Full Refresh (Optional)

```bash
dbt run --full-refresh
```

### 8. Generate Documentation

```bash
dbt docs generate
dbt docs serve
```

---

## ✅ dbt Tests Implemented

* not_null → No missing values
* unique → No duplicates
* relationships → Foreign key validation

---

## ⚡ Stretch Goals Implemented

* Incremental Models
* Backfill Strategy
* Data Freshness Checks
* Model Organization (Bronze/Silver/Gold)
* dbt Macros

---

## 📊 Sample Analytics Queries

### Total Revenue by Product

```sql
SELECT product_id, SUM(total_amount) AS revenue
FROM fct_orders
GROUP BY product_id;
```

### Customer Total Spend

```sql
SELECT customer_id, SUM(total_amount) AS total_spent
FROM fct_orders
GROUP BY customer_id;
```

---

## 🎯 Final Summary

This project demonstrates an end-to-end data pipeline:

* Raw data ingestion
* Data transformation using dbt
* Data quality validation
* Analytics-ready data modeling

🚀 Ready for real-world analytics use cases
