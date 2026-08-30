# Performance

## 1. Overview

Performance optimization is important because the fact table contains a large number of stock-price records.

The warehouse uses indexes, appropriate data types, a Star Schema, and pre-built analytical views to improve query performance.

---

## 2. Fact Table Indexing

The primary key is:

```sql
PRIMARY KEY (date_key, company_key)
```

This automatically creates an index on:

```text
date_key + company_key
```

Additional indexes are created for common query patterns.

### Company Index

```sql
CREATE INDEX IF NOT EXISTS idx_fact_company
ON warehouse.fact_stock_prices(company_key);
```

Useful when analyzing a specific company.

Example:

```sql
SELECT *
FROM warehouse.fact_stock_prices
WHERE company_key = 181;
```

### Date Index

```sql
CREATE INDEX IF NOT EXISTS idx_fact_date
ON warehouse.fact_stock_prices(date_key);
```

Useful for date-based analysis.

Example:

```sql
SELECT *
FROM warehouse.fact_stock_prices
WHERE date_key BETWEEN 20170101 AND 20171231;
```

### Company + Date Index

```sql
CREATE INDEX IF NOT EXISTS idx_fact_company_date
ON warehouse.fact_stock_prices(company_key, date_key);
```

Useful for queries that filter by company and then analyze its historical prices.

---

## 3. Appropriate Data Types

The warehouse uses appropriate PostgreSQL data types to reduce unnecessary storage and improve processing.

| Column Type    | Data Type      | Reason                         |
| -------------- | -------------- | ------------------------------ |
| Stock prices   | NUMERIC(18,6)  | Accurate financial values      |
| Trading volume | BIGINT         | Supports large trading volumes |
| Date keys      | INTEGER        | Efficient dimension joins      |
| Company keys   | INTEGER/SERIAL | Efficient surrogate keys       |
| Dates          | DATE           | Efficient date operations      |

---

## 4. Star Schema Performance

The Star Schema simplifies analytical queries by separating:

- Facts
- Dimensions

Instead of repeatedly storing company and calendar information in every stock record, the fact table stores only:

```text
date_key
company_key
```

This reduces redundancy and makes analytical joins predictable.

---

## 5. Query Performance

Use `EXPLAIN ANALYZE` to measure query performance.

Example:

```sql
EXPLAIN ANALYZE
SELECT
    company_key,
    AVG(close_price)
FROM warehouse.fact_stock_prices
GROUP BY company_key;
```

This allows the execution plan and actual execution time to be examined.

---

## 6. Analytical Views

Frequently used calculations are exposed through the analytics schema.

For example:

```text
analytics.stock_price_analysis
analytics.company_performance
```

These views provide a consistent interface for reporting tools such as Power BI.

---

## 7. Performance Metrics

The following metrics can be monitored:

| Metric               | Purpose                                  |
| -------------------- | ---------------------------------------- |
| Query execution time | Measures query speed                     |
| Rows processed       | Measures workload                        |
| Index usage          | Determines whether indexes are effective |
| ETL duration         | Measures data-loading performance        |
| Records per second   | Measures ETL throughput                  |
| Storage size         | Measures warehouse growth                |

---

## 8. ETL Performance

ETL performance can be monitored through:

```text
staging.load_metadata
```

Important fields include:

```text
records_read
records_processed
records_inserted
records_updated
records_rejected
load_start_time
load_end_time
```

ETL duration can be calculated using:

```sql
SELECT
    load_id,
    source_file,
    load_end_time - load_start_time AS load_duration,
    records_read,
    records_processed,
    records_inserted,
    records_rejected,
    status
FROM staging.load_metadata
ORDER BY load_id DESC;
```

---

## 9. Performance Optimization Strategy

The project uses the following optimization techniques:

1. **Star Schema**
2. **Primary keys**
3. **Foreign keys**
4. **Indexes**
5. **Appropriate data types**
6. **Data-quality filtering before fact loading**
7. **Analytical views**
8. **ETL load monitoring**
9. **Query execution-plan analysis**

---

## 10. Future Optimizations

As the warehouse grows, additional optimization techniques can be considered:

- Table partitioning by year
- Materialized views
- Incremental ETL
- Query result caching
- VACUUM and ANALYZE
- Index optimization
- Bulk loading
- Parallel query execution

These optimizations should be introduced based on measured performance rather than added unnecessarily.
