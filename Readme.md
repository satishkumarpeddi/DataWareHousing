# 📊 S&P 500 End-to-End Data Warehouse & Analytics Platform

> **A production-oriented Data Engineering and Data Warehousing project built with PostgreSQL, Python, Pandas, SQL, Power BI, Docker, and GitHub Actions.**

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-purple)
![Power BI](https://img.shields.io/badge/Power%20BI-Analytics-yellow)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI/CD-black)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Project Overview

This project implements an **end-to-end analytical data platform for S&P 500 historical stock-market data**.

The project starts with raw CSV files containing historical stock prices and transforms them through a controlled data pipeline into a dimensional data warehouse optimized for analytical workloads.

The final platform supports:

- Raw data ingestion
- Staging
- Data validation
- Data cleaning
- ETL
- Incremental loading
- Idempotent processing
- Slowly Changing Dimensions
- Star-schema dimensional modeling
- Data-quality testing
- ETL audit logging
- Error handling
- SQL analytics
- Python analytics
- Query optimization
- Power BI dashboards
- Dockerized infrastructure
- Automated testing
- GitHub Actions CI/CD

The primary objective is not simply to store stock data.

The objective is to demonstrate how a **real-world analytical data platform is designed, implemented, validated, optimized, and consumed**.

---

# 🎯 Project Objectives

The project is designed to demonstrate practical knowledge of:

### Data Warehousing

- Dimensional modeling
- Star schema
- Fact tables
- Dimension tables
- Fact grain
- Surrogate keys
- Natural keys
- Slowly Changing Dimensions
- Historical tracking
- Conformed dimensions
- Additive and semi-additive measures

### Data Engineering

- ETL pipelines
- Batch processing
- Incremental processing
- Idempotent pipelines
- Data validation
- Error handling
- Audit logging
- Data lineage
- Pipeline monitoring

### Database Engineering

- PostgreSQL
- Schemas
- Primary keys
- Foreign keys
- Unique constraints
- Indexes
- Composite indexes
- Transactions
- Views
- Materialized views
- Partitioning
- Query optimization
- `EXPLAIN ANALYZE`

### Programming

- Python
- Pandas
- SQL
- Logging
- Exception handling
- Unit testing

### Business Intelligence

- Power BI
- Star-schema semantic models
- DAX
- KPIs
- Time intelligence
- Interactive dashboards

### DevOps

- Git
- GitHub
- Docker
- Docker Compose
- GitHub Actions
- Continuous Integration

---

# 🏗️ High-Level Architecture

```text
                         ┌──────────────────────┐
                         │   S&P 500 CSV DATA   │
                         │                      │
                         │ date                 │
                         │ open                 │
                         │ high                 │
                         │ low                  │
                         │ close                │
                         │ volume               │
                         │ ticker               │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      RAW LAYER       │
                         │                      │
                         │ Original Source Data │
                         └──────────┬───────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │         STAGING            │
                     │                            │
                     │ staging.stock_prices       │
                     │ staging.load_metadata      │
                     └─────────────┬──────────────┘
                                   │
                                   ▼
                     ┌────────────────────────────┐
                     │       DATA QUALITY         │
                     │                            │
                     │ NULL checks                │
                     │ Duplicate checks           │
                     │ Price validation           │
                     │ Date validation            │
                     │ Volume validation          │
                     └─────────────┬──────────────┘
                                   │
                                   ▼
                     ┌────────────────────────────┐
                     │        ETL ENGINE          │
                     │                            │
                     │ Python + Pandas + SQL      │
                     │ Extract                    │
                     │ Transform                  │
                     │ Validate                   │
                     │ Load                       │
                     └─────────────┬──────────────┘
                                   │
                                   ▼
             ┌─────────────────────────────────────────┐
             │             DATA WAREHOUSE              │
             │                                         │
             │  ┌──────────────┐  ┌──────────────┐     │
             │  │   dim_date   │  │ dim_company  │     │
             │  └──────┬───────┘  └──────┬───────┘     │
             │         │                 │             │
             │         └────────┬────────┘             │
             │                  ▼                      │
             │       ┌─────────────────────┐           │
             │       │ fact_stock_prices   │           │
             │       └─────────────────────┘           │
             |                                         │
             │  ETL Audit / Error Logging              │
             └──────────────────┬──────────────────────┘
                                │
                                ▼
                     ┌────────────────────────────┐
                     │      ANALYTICS LAYER       │
                     │                            │
                     │ Daily Returns              │
                     │ Monthly Performance        │
                     │ Moving Averages            │
                     │ Volatility                 │
                     │ Company Rankings           │
                     │ Sector Performance         │
                     └─────────────┬──────────────┘
                                   │
                     ┌─────────────┼─────────────┐
                     ▼             ▼             ▼
                 PostgreSQL      Python       Power BI
                  Analytics      Analysis     Dashboard
                     │             │             │
                     └─────────────┼─────────────┘
                                   ▼
                           Business Insights
```

---

# 🧱 Data Architecture

The platform is divided into logical layers.

```text
Source
  ↓
Raw
  ↓
Staging
  ↓
Quality
  ↓
Transformation
  ↓
Warehouse
  ↓
Analytics
  ↓
BI
```

Each layer has a specific responsibility.

---

# 1️⃣ Source Layer

The source is historical S&P 500 stock data.

Typical columns:

```text
date
open
high
low
close
volume
Name
```

Example:

```text
2013-02-08,15.07,15.12,14.63,14.75,8407500,AAL
```

Where:

| Column   | Meaning                 |
| -------- | ----------------------- |
| `date`   | Trading date            |
| `open`   | Opening price           |
| `high`   | Highest price           |
| `low`    | Lowest price            |
| `close`  | Closing price           |
| `volume` | Number of shares traded |
| `Name`   | Stock ticker            |

The source layer should remain as close as possible to the original source.

---

# 2️⃣ Raw Layer

The raw layer preserves source information before significant transformation.

The principle is:

> Never destroy the original source unnecessarily.

This allows the pipeline to be reprocessed if a transformation rule changes.

---

# 3️⃣ Staging Layer

The staging layer is the first controlled database representation of incoming data.

Example:

```sql
staging.stock_prices
```

Conceptually:

```text
staging.stock_prices
--------------------------------
date
open_price
high_price
low_price
close_price
volume
ticker
load_id
loaded_at
```

The staging layer is temporary/intermediate compared with the dimensional warehouse.

---

# Why staging exists

Without staging:

```text
CSV
 ↓
Warehouse
```

With staging:

```text
CSV
 ↓
Staging
 ↓
Validation
 ↓
Transformation
 ↓
Warehouse
```

Staging provides:

- source isolation
- validation
- debugging
- reprocessing
- traceability
- controlled transformation

---

# 4️⃣ Data Quality Layer

Before records reach the warehouse, they are validated.

Example rules:

### Null validation

```sql
WHERE date IS NULL
```

or:

```sql
WHERE ticker IS NULL
```

### Price validation

```text
open > 0
high > 0
low > 0
close > 0
```

### High/Low relationship

```text
high >= low
```

### OHLC consistency

```text
high >= open
high >= close
low <= open
low <= close
```

### Volume validation

```text
volume >= 0
```

### Duplicate validation

```text
ticker + date
```

must identify one stock-day record.

---

# 5️⃣ ETL Layer

The ETL pipeline performs:

```text
Extract
   ↓
Transform
   ↓
Validate
   ↓
Load
```

---

## Extract

Read source data.

```python
import pandas as pd

df = pd.read_csv("data/raw/stocks.csv")
```

---

## Transform

Normalize columns:

```python
df = df.rename(columns={
    "Name": "ticker",
    "open": "open_price",
    "high": "high_price",
    "low": "low_price",
    "close": "close_price"
})
```

Convert dates:

```python
df["date"] = pd.to_datetime(df["date"])
```

---

## Validate

```python
assert df["date"].notna().all()
assert df["ticker"].notna().all()
assert (df["high_price"] >= df["low_price"]).all()
```

---

## Load

Validated records are loaded into PostgreSQL.

---

# 6️⃣ Data Warehouse

The core warehouse follows a **Star Schema**.

```text
                    dim_date
                       │
                       │
                       ▼
                fact_stock_prices
                       ▲
                       │
                       │
                  dim_company
```

---

# ⭐ Star Schema

The central fact table stores measurable events.

Dimension tables describe those events.

---

# 📅 Dimension: `dim_date`

Example:

```text
dim_date
--------------------------------
date_key
full_date
day
month
month_name
quarter
year
day_of_week
day_name
is_weekend
```

Example:

```text
date_key | full_date  | month | quarter | year
---------|------------|-------|---------|------
20260105 | 2026-01-05 | 1     | 1       | 2026
```

---

# 🏢 Dimension: `dim_company`

Example:

```text
dim_company
--------------------------------
company_key
ticker
company_name
sector
industry
effective_date
expiry_date
is_current
```

The `company_key` is a surrogate key.

---

# 📈 Fact: `fact_stock_prices`

Example:

```text
fact_stock_prices
--------------------------------
date_key
company_key
open_price
high_price
low_price
close_price
volume
```

---

# 🔑 Fact Grain

The grain is:

> **One row represents one company's stock price information for one trading day.**

Therefore:

```text
Company + Date = One Fact
```

This is critical.

If the grain is not clearly defined, the fact table can become inconsistent.

---

# 🔑 Surrogate Keys

The warehouse uses surrogate keys such as:

```text
company_key = 1
date_key = 20260105
```

instead of relying exclusively on source identifiers.

Benefits:

- warehouse independence
- easier historical tracking
- SCD support
- stable joins
- better dimensional modeling

---

# 🔄 Incremental ETL

A production-style pipeline should avoid processing the entire dataset unnecessarily.

Instead:

```text
Existing Warehouse
        +
New Source Data
        ↓
Identify New/Changed Records
        ↓
Validate
        ↓
Load
```

---

# Watermark Strategy

A watermark tracks the latest successfully processed value.

Example:

```text
last_processed_date = 2026-08-25
```

New records:

```text
date > 2026-08-25
```

are candidates for processing.

---

# Idempotency

A pipeline is idempotent when executing it repeatedly produces the same final warehouse state rather than creating duplicates.

Example:

```text
First execution:
10,000 records → inserted

Second execution:
10,000 records → already exists

Third execution:
10,000 records → already exists
```

This can be supported with constraints such as:

```sql
UNIQUE (date_key, company_key)
```

and controlled upsert logic.

---

# 🔁 Upsert

Conceptually:

```sql
INSERT INTO warehouse.fact_stock_prices (...)
VALUES (...)
ON CONFLICT (date_key, company_key)
DO UPDATE SET
    close_price = EXCLUDED.close_price,
    volume = EXCLUDED.volume;
```

The exact conflict behavior depends on the business requirement.

---

# 🕰️ Slowly Changing Dimensions

Company attributes can change.

For example:

```text
Company
Sector
Industry
```

may change over time.

SCD Type 2 preserves history.

---

## Before change

```text
company_key | ticker | sector       | is_current
------------|--------|--------------|-----------
101         | XYZ    | Technology   | true
```

After change:

```text
company_key | ticker | sector       | is_current
------------|--------|--------------|-----------
101         | XYZ    | Technology   | false
102         | XYZ    | Finance      | true
```

Historical records remain available.

---

# 🧾 ETL Audit

The system records pipeline executions.

Example:

```text
etl_audit
----------------------------------------
audit_id
process_name
start_time
end_time
records_read
records_inserted
records_updated
records_rejected
status
error_message
```

Example:

```text
process_name : stock_price_load
records_read : 150000
inserted     : 12000
updated      : 500
rejected     : 25
status       : SUCCESS
```

---

# ❌ ETL Error Handling

Invalid records should be captured rather than silently discarded.

Example:

```text
etl_errors
----------------------------------------
error_id
load_id
record_identifier
error_type
error_message
raw_data
created_at
```

Example error:

```text
error_type:
INVALID_PRICE

error_message:
high_price cannot be lower than low_price
```

---

# 📊 Analytics Layer

The analytics layer converts warehouse data into business-oriented datasets.

Potential objects:

```text
analytics.daily_returns
analytics.monthly_performance
analytics.company_performance
analytics.market_summary
analytics.volume_analysis
analytics.volatility_analysis
```

---

# 📈 Daily Returns

A basic daily return:

```text
(close_today - close_previous_day)
/
close_previous_day
```

Example:

```text
Previous close = 100
Current close  = 105

Return = 5%
```

SQL can use window functions such as:

```sql
LAG(close_price)
OVER (
    PARTITION BY company_key
    ORDER BY date_key
)
```

---

# 📉 Moving Average

Example:

```text
20-day moving average
50-day moving average
200-day moving average
```

These can be calculated using window functions.

---

# 📊 Volatility

Historical volatility can be derived from returns.

Conceptually:

```text
Daily Returns
      ↓
Statistical dispersion
      ↓
Volatility
```

This provides a measure of how widely prices fluctuate.

---

# 🏆 Company Ranking

Analytics can rank companies based on:

- total return
- average return
- trading volume
- volatility
- price appreciation
- drawdown

---

# 🏭 Sector Analytics

If sector information is available:

```text
Technology
Healthcare
Finance
Energy
Consumer
Industrial
...
```

we can compare sector performance.

---

# ⚡ Query Optimization

The project will demonstrate database performance engineering.

Example:

```sql
EXPLAIN ANALYZE
SELECT ...
```

The query plan helps identify:

- sequential scans
- index scans
- expensive joins
- sorting
- aggregation cost
- execution time

---

# 🗂️ Indexing Strategy

Potential indexes include:

```sql
CREATE INDEX idx_fact_company_date
ON warehouse.fact_stock_prices(company_key, date_key);
```

and:

```sql
CREATE INDEX idx_fact_date
ON warehouse.fact_stock_prices(date_key);
```

Indexes must be designed based on actual query patterns.

More indexes are not automatically better.

---

# 🧩 Composite Indexes

Because the fact grain is:

```text
company + date
```

a composite index can be highly useful for queries filtering by both fields.

Example:

```text
(company_key, date_key)
```

---

# 🧱 Partitioning

As fact tables become very large, partitioning can be considered.

A possible strategy:

```text
fact_stock_prices
        │
        ├── 2013
        ├── 2014
        ├── 2015
        ├── ...
        └── 2026
```

Partitioning strategy should be based on workload and table size rather than added simply for appearance.

---

# 🧠 Materialized Views

Frequently requested analytical results can be precomputed.

Example:

```text
analytics.monthly_performance
```

A materialized view can reduce repeated expensive calculations.

However, refresh strategy must also be considered.

---

# 🐍 Python ETL Architecture

The Python ETL code should be modular.

```text
etl/
│
├── config.py
├── extract.py
├── transform.py
├── validate.py
├── load.py
├── pipeline.py
└── logger.py
```

---

# `extract.py`

Responsible for:

```text
Reading CSV
Reading source data
Basic ingestion
```

---

# `transform.py`

Responsible for:

```text
Column normalization
Data type conversion
Cleaning
Standardization
Derived fields
```

---

# `validate.py`

Responsible for:

```text
Null checks
Range checks
Duplicate detection
Business rules
```

---

# `load.py`

Responsible for:

```text
PostgreSQL connection
Dimension loading
Fact loading
Upserts
Transactions
```

---

# `pipeline.py`

Orchestrates the complete process:

```text
Extract
   ↓
Transform
   ↓
Validate
   ↓
Load Dimensions
   ↓
Load Facts
   ↓
Update Audit
```

---

# 📝 Logging

The ETL pipeline should produce structured logs.

Example:

```text
2026-08-26 10:00:01 INFO Starting pipeline
2026-08-26 10:00:03 INFO Reading source file
2026-08-26 10:00:05 INFO 150000 records loaded
2026-08-26 10:00:06 INFO Running validation
2026-08-26 10:00:07 INFO 149975 records passed
2026-08-26 10:00:08 INFO Loading dimensions
2026-08-26 10:00:10 INFO Loading facts
2026-08-26 10:00:14 INFO Pipeline completed successfully
```

---

# 🧪 Testing Strategy

Testing occurs at multiple levels.

## Unit Tests

Test individual Python functions.

Example:

```text
test_date_conversion()
test_price_validation()
test_duplicate_detection()
```

---

## Data Quality Tests

Verify:

```text
No NULL primary keys
No duplicate company/date facts
No invalid prices
No invalid dates
No broken foreign keys
```

---

## Integration Tests

Verify:

```text
Python
   ↓
PostgreSQL
   ↓
Warehouse
```

works as a complete pipeline.

---

# 🐳 Docker Architecture

The environment can be containerized.

Example:

```text
docker-compose.yml

        ┌─────────────────┐
        │   PostgreSQL    │
        └────────┬────────┘
                 │
                 │
        ┌────────▼────────┐
        │    Python ETL   │
        └─────────────────┘
```

Optional services can include pgAdmin.

---

# 🔐 Configuration

Sensitive configuration should not be hardcoded.

Use environment variables:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

A `.env.example` file should document required variables without exposing real credentials.

---

# 🔄 CI/CD

GitHub Actions can execute checks automatically.

```text
Developer Push
      ↓
GitHub Actions
      ↓
Install Dependencies
      ↓
Run Python Tests
      ↓
Run Quality Checks
      ↓
Validate Project
      ↓
PASS / FAIL
```

---

# 📊 Power BI Architecture

Power BI connects to the analytical warehouse.

Recommended model:

```text
                 dim_date
                    │
                    │
                    ▼
             fact_stock_prices
                    ▲
                    │
                    │
               dim_company
```

The Power BI model should preserve the dimensional structure rather than flattening everything unnecessarily.

---

# 📈 Power BI Dashboard

## Page 1 — Executive Overview

KPIs:

```text
Total Companies
Total Trading Records
Average Closing Price
Total Trading Volume
Average Daily Return
Market Volatility
```

Charts:

```text
Price Trend
Volume Trend
Top Performers
Worst Performers
Sector Performance
```

---

# 📈 Page 2 — Company Analysis

Filters:

```text
Ticker
Date
Sector
Industry
```

Metrics:

```text
Current Price
Average Price
Daily Return
Total Return
Volatility
52-Week High
52-Week Low
Trading Volume
```

---

# 📊 Page 3 — Market Analysis

Visualizations:

```text
Market trend
Sector comparison
Monthly returns
Annual returns
Volume distribution
Volatility comparison
```

---

# 📅 Page 4 — Time Analysis

Analyze:

```text
Year
Quarter
Month
Trading day
```

This demonstrates the importance of the date dimension.

---

# 📁 Final Repository Structure

```text
DataWareHousing/
│
├── data/
│   └── raw/
│       └── stocks.csv
│
├── sql/
│   ├── 01_database.sql
│   ├── 02_schemas.sql
│   ├── 03_staging.sql
│   ├── 04_dimensions.sql
│   ├── 05_facts.sql
│   ├── 06_etl.sql
│   ├── 07_data_quality.sql
│   ├── 08_analytics.sql
│   └── 09_indexes.sql
│
├── etl/
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   ├── pipeline.py
│   └── logger.py
│
├── analytics/
│   ├── daily_returns.sql
│   ├── monthly_performance.sql
│   ├── company_performance.sql
│   ├── market_summary.sql
│   └── volatility.sql
│
├── tests/
│   ├── test_etl.py
│   ├── test_quality.py
│   └── test_transformations.py
│
├── powerbi/
│   └── S&P500_Analytics.pbix
│
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── etl_pipeline.md
│   ├── data_quality.md
│   └── performance.md
│
├── docker/
│   └── Dockerfile
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── schema.sql
├── README.md
└── LICENSE
```

---

# 🔍 Data Flow

The complete data flow is:

```text
S&P 500 CSV
     │
     ▼
Raw Dataset
     │
     ▼
Staging Table
     │
     ▼
Data Validation
     │
     ├────────────── FAIL ──────► ETL Error Table
     │
     ▼ PASS
Transformation
     │
     ▼
Dimension Loading
     │
     ▼
Fact Loading
     │
     ▼
Audit Logging
     │
     ▼
Analytics Views
     │
     ├──────────────► SQL
     │
     ├──────────────► Python
     │
     └──────────────► Power BI
```

---

# 🔐 Data Integrity

The warehouse should enforce integrity at the database level.

Examples:

```text
Primary Keys
Foreign Keys
Unique Constraints
NOT NULL
CHECK Constraints
```

Example business rule:

```sql
CHECK (high_price >= low_price)
```

Database constraints protect against bad data even if an application-level validation fails.

---

# 🔄 Transaction Management

Loading related warehouse data should use transactions where appropriate.

Conceptually:

```text
BEGIN
   │
   ├── Load dimensions
   ├── Load facts
   ├── Write audit
   │
   ▼
COMMIT
```

If a critical operation fails:

```text
ROLLBACK
```

This prevents partially committed warehouse states.

---

# 🧬 Data Lineage

The project documents how a warehouse column originates.

Example:

```text
CSV:
Name
  ↓
staging.stock_prices:
ticker
  ↓
dim_company:
ticker
  ↓
Power BI:
Company Ticker
```

Another example:

```text
CSV:
close
  ↓
staging:
close_price
  ↓
fact_stock_prices:
close_price
  ↓
analytics:
daily_return
  ↓
Power BI:
Performance %
```

---

# 📚 Data Dictionary

A data dictionary documents every important field.

Example:

| Table               | Column        | Type    | Description           |
| ------------------- | ------------- | ------- | --------------------- |
| `dim_date`          | `date_key`    | INTEGER | Date surrogate key    |
| `dim_date`          | `full_date`   | DATE    | Calendar date         |
| `dim_company`       | `company_key` | INTEGER | Company surrogate key |
| `dim_company`       | `ticker`      | VARCHAR | Stock ticker          |
| `fact_stock_prices` | `open_price`  | NUMERIC | Opening price         |
| `fact_stock_prices` | `close_price` | NUMERIC | Closing price         |
| `fact_stock_prices` | `volume`      | BIGINT  | Trading volume        |

---

# 🧠 Important Data Warehouse Concepts Demonstrated

## OLTP vs OLAP

### OLTP

Designed for:

```text
Transactions
Fast writes
Operational applications
```

### OLAP

Designed for:

```text
Analytics
Aggregations
Historical analysis
Reporting
BI
```

This project is primarily an **OLAP/data warehouse system**.

---

# ⭐ Why Star Schema?

A star schema makes analytical queries easier to understand.

Instead of storing everything in one enormous table:

```text
stock_data
--------------------------------
date
ticker
company
sector
month
quarter
year
open
high
low
close
volume
...
```

we separate descriptive information:

```text
dim_date
dim_company
fact_stock_prices
```

This reduces unnecessary repetition and creates a clearer analytical model.

---

# ❄️ Star vs Snowflake

### Star

```text
       dim_date
          │
          ▼
       FACT
          ▲
          │
    dim_company
```

### Snowflake

```text
dim_company
     │
     ▼
dim_sector
     │
     ▼
dim_industry
```

The project primarily uses the **star schema** because it is straightforward and highly suitable for BI workloads.

---

# 📐 Grain

Grain must be declared before designing the fact table.

Our grain:

```text
One company
+
One trading date
=
One fact record
```

This single decision affects:

- primary keys
- uniqueness
- ETL
- aggregations
- indexes
- analytics

---

# 🧮 Measures

Measures in the fact table include:

```text
open_price
high_price
low_price
close_price
volume
```

Some measures are additive under certain dimensions while others require special treatment.

For example, summing closing prices across companies is usually not meaningful.

Volume, however, can generally be aggregated across companies or time depending on the business question.

---

# 🚨 Common Failure Scenarios

## Duplicate Fact

Error concept:

```text
same company
+
same date
```

Solution:

```text
UNIQUE(company_key, date_key)
```

plus appropriate ETL logic.

---

## Header Imported as Data

Example:

```text
order_id
```

being inserted where an integer is expected.

Root cause:

```text
CSV header interpreted as a data row.
```

Solution:

```text
Correct CSV import/header handling.
```

---

## Schema Already Exists

Example:

```text
schema "staging" already exists
```

This is not necessarily a serious problem.

Use:

```sql
CREATE SCHEMA IF NOT EXISTS staging;
```

when appropriate.

---

## ON CONFLICT Failure

`ON CONFLICT` requires a matching unique or exclusion constraint.

Therefore:

```sql
ON CONFLICT (company_key, date_key)
```

requires an appropriate constraint/index on those columns.

---

# 🛠️ Technologies

| Technology     | Purpose                |
| -------------- | ---------------------- |
| PostgreSQL     | Data warehouse         |
| SQL            | Modeling and analytics |
| Python         | ETL                    |
| Pandas         | Data transformation    |
| Power BI       | Visualization          |
| Docker         | Environment            |
| Git            | Version control        |
| GitHub         | Source control         |
| GitHub Actions | CI                     |
| pytest         | Testing                |

---

# 🚀 Getting Started

## Prerequisites

Install:

- PostgreSQL
- Python 3.x
- Git
- Docker
- Power BI Desktop

---

## Clone Repository

```bash
git clone https://github.com/satishkumarpeddi/DataWareHousing.git
cd DataWareHousing
```

---

# 🐍 Create Python Environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Configure Environment

Create:

```text
.env
```

based on:

```text
.env.example
```

Example:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sp500_dw
DB_USER=postgres
DB_PASSWORD=your_password
```

Never commit `.env`.

---

# 🗄️ Database Setup

Create the PostgreSQL database.

Then execute the SQL scripts in the intended order:

```text
01_database.sql
02_schemas.sql
03_staging.sql
04_dimensions.sql
05_facts.sql
06_etl.sql
07_data_quality.sql
08_analytics.sql
09_indexes.sql
```

---

# ▶️ Run ETL

Example:

```bash
python -m etl.pipeline
```

The pipeline should:

```text
Read source
 ↓
Validate
 ↓
Transform
 ↓
Load staging
 ↓
Load dimensions
 ↓
Load facts
 ↓
Run quality checks
 ↓
Write audit
```

---

# 🐳 Docker Setup

Run:

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

Stop:

```bash
docker compose down
```

---

# 🧪 Run Tests

```bash
pytest
```

Verbose:

```bash
pytest -v
```

---

# 📊 Connect Power BI

Connect Power BI to PostgreSQL.

Recommended source:

```text
analytics
```

or selected warehouse tables/views.

Build relationships around:

```text
dim_date
dim_company
fact_stock_prices
```

---

# 📈 Example Analytical Questions

The warehouse should answer questions such as:

### Company Performance

- Which companies generated the highest returns?
- Which companies experienced the largest losses?
- Which companies have the highest volatility?
- Which stocks have the highest trading volume?

### Time Analysis

- Which year had the strongest performance?
- Which months produced the highest returns?
- How does volume change over time?
- How does a stock's price compare with its moving average?

### Sector Analysis

- Which sectors performed best?
- Which sectors have the highest volatility?
- How does average return differ by sector?

### Market Analysis

- What is the overall market trend?
- Which companies dominate trading volume?
- How concentrated are returns?
- Which stocks experienced the largest drawdowns?

---

# 📊 Expected Final Deliverables

The completed project should contain:

```text
✓ PostgreSQL data warehouse
✓ Staging layer
✓ Star schema
✓ Dimension tables
✓ Fact table
✓ Incremental ETL
✓ Idempotent loading
✓ SCD Type 2
✓ Data-quality framework
✓ Error handling
✓ ETL audit
✓ SQL analytics
✓ Python ETL
✓ Python tests
✓ Query optimization
✓ Indexing
✓ Optional partitioning
✓ Materialized analytics
✓ Power BI dashboard
✓ Docker environment
✓ GitHub Actions
✓ Technical documentation
✓ Data dictionary
✓ Architecture documentation
```

---

# 🏆 Skills Demonstrated

After completing the project, the repository demonstrates practical experience with:

```text
Data Warehousing
        ↓
Dimensional Modeling
        ↓
ETL / ELT
        ↓
Data Quality
        ↓
Incremental Processing
        ↓
PostgreSQL
        ↓
Python / Pandas
        ↓
Analytics
        ↓
Power BI
        ↓
Docker
        ↓
Testing
        ↓
CI/CD
```

---

# 💼 Resume Project Description

**S&P 500 End-to-End Data Warehouse & Analytics Platform**

Designed and implemented an end-to-end analytical data warehouse for historical S&P 500 market data using PostgreSQL, Python, Pandas, and Power BI. Built a layered architecture consisting of source, staging, quality, dimensional warehouse, and analytics layers. Implemented star-schema modeling, incremental and idempotent ETL, SCD Type 2 historical tracking, data-quality validation, audit logging, error handling, analytical SQL, query optimization, Docker-based infrastructure, automated testing, and CI/CD with GitHub Actions.

---

# 🎤 Interview Explanation

A concise explanation of the project:

> "I built an end-to-end S&P 500 analytical data warehouse. Raw CSV data enters a staging layer where it is validated and transformed. Python and SQL handle the ETL process. The cleaned data is loaded into a PostgreSQL star schema consisting of date and company dimensions and a stock-price fact table. I implemented incremental and idempotent loading, SCD Type 2 for historical dimension changes, data-quality checks, error handling, and ETL audit logging. I then built analytical views for returns, volatility, moving averages, and company and sector performance, which are consumed by Power BI. The environment is containerized with Docker and validated through automated tests and GitHub Actions."

---

# 🧠 Key Lessons

The most important lessons from this project are:

### 1. Always define the grain first.

```text
What does one row represent?
```

### 2. Separate raw data from transformed data.

```text
Source ≠ Staging ≠ Warehouse
```

### 3. Data quality belongs inside the pipeline.

Bad data should not silently enter analytical tables.

### 4. ETL must be restartable.

A production pipeline should survive failures and safely run again.

### 5. Constraints are part of data quality.

Database integrity should not depend entirely on Python.

### 6. Performance must be measured.

Use:

```sql
EXPLAIN ANALYZE
```

rather than assuming an optimization is useful.

### 7. BI depends on good modeling.

A beautiful dashboard cannot compensate for a poorly designed warehouse.

---

# 🚀 Future Enhancements

Possible future improvements include:

- Real-time market data ingestion
- Kafka
- Apache Spark
- Airflow
- dbt
- Cloud storage
- AWS S3
- Azure Data Lake
- Snowflake
- BigQuery
- Databricks
- CDC pipelines
- Streaming analytics
- ML-based forecasting
- Anomaly detection
- Data catalog
- Advanced observability

These are intentionally considered future extensions rather than unnecessary complexity in the initial implementation.

---

# 📜 Project Development Philosophy

This project is being developed as a **learning-by-building system**.

The implementation process follows:

```text
Understand
    ↓
Design
    ↓
Implement
    ↓
Test
    ↓
Break
    ↓
Debug
    ↓
Optimize
    ↓
Document
```

The goal is not simply to produce a working repository.

The goal is to understand **why each architectural decision exists**.

---

# 🏁 Final Vision

The final platform represents the complete lifecycle:

```text
                   RAW DATA
                      │
                      ▼
                   STAGING
                      │
                      ▼
                DATA QUALITY
                      │
                      ▼
                     ETL
                      │
                      ▼
              DATA WAREHOUSE
                      │
             ┌────────┼────────┐
             ▼        ▼        ▼
            SQL     Python   Analytics
             │        │        │
             └────────┼────────┘
                      ▼
                   POWER BI
                      │
                      ▼
              BUSINESS INSIGHTS

        ┌──────────────────────────┐
        │ Supporting Infrastructure│
        │                          │
        │ Docker                   │
        │ Testing                  │
        │ GitHub Actions           │
        │ Logging                  │
        │ Documentation            │
        └──────────────────────────┘
```

The final result is intended to demonstrate not only **SQL and database knowledge**, but an understanding of the complete **Data Engineering → Data Warehouse → Analytics → Business Intelligence lifecycle**.

---

# ⭐ Project Status

```text
[████████████████████░░░░░░░░░░] In Development
```

The existing repository contains the foundational warehouse implementation.

The project will be progressively upgraded toward the architecture documented above.

---

# 👨‍💻 Author

**Satish Kumar Peddi**

GitHub:

`https://github.com/satishkumarpeddi`

Repository:

`https://github.com/satishkumarpeddi/DataWareHousing`

---

# 📄 License

This project is licensed under the MIT License.

---

## ⭐ If this project helps you understand Data Warehousing

Consider starring the repository and following the development journey.

The project is being built as a practical demonstration of **Data Warehousing, Data Engineering, SQL, Python, PostgreSQL, ETL, BI, testing, and DevOps**.
