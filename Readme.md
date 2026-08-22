# 📊 S&P 500 Stock Market Data Warehouse

> **An end-to-end Data Warehouse project built with PostgreSQL, SQL, ETL, dimensional modeling, and Power BI to transform raw S&P 500 historical stock data into an analytics-ready warehouse.**

---

## 🚀 Project Overview

This project demonstrates how raw financial market data can be transformed into a structured **data warehouse using a Star Schema** and then exposed through **business-focused analytics and Power BI visualizations**.

The pipeline separates raw ingestion from analytical storage:

```text
Raw CSV
   │
   ▼
┌────────────────────┐
│      STAGING       │
│ stock_prices       │
└─────────┬──────────┘
          │
          │ ETL
          ▼
┌─────────────────────────────────────────────┐
│              DATA WAREHOUSE                 │
│                                             │
│  dim_date ───────────────┐                 │
│                          │                 │
│  dim_company ────────────┼──► fact_stock   │
│                          │    _prices      │
└──────────────────────────┴─────────────────┘
          │
          ▼
┌────────────────────┐
│      ANALYTICS     │
│       SQL          │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│      POWER BI      │
│ Interactive Report │
└────────────────────┘
```

---

## 🎯 Project Objectives

- Build a complete PostgreSQL data warehouse from raw CSV data.
- Implement a **staging layer** for raw data ingestion.
- Design and implement a **Star Schema**.
- Build reusable SQL-based ETL logic.
- Implement data-quality checks.
- Prevent duplicate fact records through database constraints.
- Add ETL audit logging and error tracking.
- Create analytical queries for stock performance, volume, returns, and volatility.
- Connect the warehouse to Power BI.
- Build an interactive financial-market dashboard.
- Demonstrate practical data-engineering and data-warehousing concepts.

---

## 🗂️ Dataset

The source dataset contains historical stock-market records with fields representing:

| Column | Description |
|---|---|
| `date` | Trading date |
| `open_price` | Opening price |
| `high_price` | Highest price during the trading day |
| `low_price` | Lowest price during the trading day |
| `close_price` | Closing price |
| `volume` | Trading volume |
| `ticker` | Stock ticker symbol |

Example:

```text
date        open_price  high_price  low_price  close_price  volume    ticker
2013-02-08  15.07       15.12       14.63      14.75        8407500   AAL
2013-02-11  14.89       15.01       14.26      14.46        8882000   AAL
2013-02-12  14.45       14.51       14.10      14.27        8126000   AAL
```

---

# 🏗️ Data Warehouse Architecture

The warehouse follows a **Star Schema**.

```text
                         ┌──────────────────┐
                         │    dim_date      │
                         ├──────────────────┤
                         │ date_key         │
                         │ full_date        │
                         │ year             │
                         │ quarter          │
                         │ month            │
                         │ month_name       │
                         │ day              │
                         │ day_name         │
                         │ week_of_year     │
                         └────────┬─────────┘
                                  │
                                  │ 1 : N
                                  ▼
┌──────────────────┐       ┌──────────────────────────┐
│   dim_company    │       │   fact_stock_prices      │
├──────────────────┤       ├──────────────────────────┤
│ company_key PK   │───┐   │ stock_price_key PK       │
│ ticker           │   └──►│ date_key FK              │
└──────────────────┘       │ company_key FK           │
                           │ open_price               │
                           │ high_price               │
                           │ low_price                │
                           │ close_price              │
                           │ volume                   │
                           └──────────────────────────┘
```

### Fact Table

`warehouse.fact_stock_prices`

Contains measurable stock-market events:

- Opening price
- Highest price
- Lowest price
- Closing price
- Trading volume

### Dimension Tables

`warehouse.dim_date`

Provides time-based analysis:

- Year
- Quarter
- Month
- Day
- Week

`warehouse.dim_company`

Provides stock-level analysis:

- Company surrogate key
- Ticker symbol

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **PostgreSQL** | Data warehouse database |
| **pgAdmin 4** | Database administration and SQL development |
| **SQL** | Data transformation and analytics |
| **PL/pgSQL** | ETL procedure |
| **Power BI** | Interactive visualization |
| **CSV** | Source data |
| **Git/GitHub** | Version control and portfolio management |

---

# 🔄 ETL Pipeline

The ETL process follows:

```text
Extract
   │
   ▼
CSV → staging.stock_prices
   │
   ▼
Transform
   │
   ├── Validate records
   ├── Remove duplicates
   ├── Generate date keys
   ├── Generate company keys
   └── Transform source fields
   │
   ▼
Load
   │
   ├── dim_company
   ├── dim_date
   └── fact_stock_prices
```

The main procedure is:

```sql
CALL warehouse.load_stock_data();
```

The ETL is designed to be **idempotent** for already-loaded stock/date combinations.

---

# 🧪 Data Quality

The project includes checks for:

### NULL values

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE date IS NULL) AS null_dates,
    COUNT(*) FILTER (WHERE ticker IS NULL) AS null_tickers,
    COUNT(*) FILTER (WHERE open_price IS NULL) AS null_open,
    COUNT(*) FILTER (WHERE close_price IS NULL) AS null_close
FROM staging.stock_prices;
```

### Invalid prices

```sql
SELECT *
FROM staging.stock_prices
WHERE open_price <= 0
   OR high_price <= 0
   OR low_price <= 0
   OR close_price <= 0;
```

### Invalid high/low relationships

```sql
SELECT *
FROM staging.stock_prices
WHERE high_price < low_price;
```

### Duplicate stock/date combinations

```sql
SELECT
    date,
    ticker,
    COUNT(*) AS duplicate_count
FROM staging.stock_prices
GROUP BY date, ticker
HAVING COUNT(*) > 1;
```

---

# 🔐 Data Integrity

The fact table enforces uniqueness for each stock on each trading date:

```sql
UNIQUE (date_key, company_key)
```

This prevents the same stock/date record from being loaded multiple times.

The ETL uses:

```sql
ON CONFLICT (date_key, company_key)
DO NOTHING;
```

to safely handle repeated executions.

---

# 📝 ETL Audit Logging

The warehouse contains:

```text
warehouse.etl_audit
```

It records:

- Audit ID
- Process name
- Start time
- End time
- Status
- Rows loaded
- Error message

Example:

```text
audit_id | process_name   | status  | rows_loaded
---------+----------------+---------+------------
1        | load_stock_data| SUCCESS | ...
2        | load_stock_data| SUCCESS | ...
```

This provides basic operational monitoring for the ETL process.

---

# 📈 Business Analytics

The warehouse supports analytical questions such as:

### Stock Performance

- What is the average closing price by company?
- Which stocks reached the highest closing price?
- Which stocks had the lowest closing price?
- Which stocks performed best over the available period?

### Trading Activity

- Which companies have the highest total trading volume?
- What is the average daily trading volume?
- Which months had the highest market activity?

### Returns

Daily return is calculated as:

```text
Daily Return % =
((Close Price - Open Price) / Open Price) × 100
```

This allows analysis of:

- Average daily return
- Biggest single-day gains
- Biggest single-day losses
- Overall return

### Volatility

A simple daily volatility measure is:

```text
Volatility % =
((High Price - Low Price) / Low Price) × 100
```

This can be used to identify stocks with larger intraday price movements.

---

# 📊 Power BI Dashboard

The warehouse is designed to connect directly to **Power BI**.

The planned dashboard includes:

### KPI Cards

- Total Stocks
- Trading Days
- Total Records
- Total Trading Volume
- Average Closing Price

### Visualizations

📈 **Stock Price Trend**

Track closing prices over time.

📊 **Top 10 Stocks**

Rank stocks by average closing price.

📊 **Trading Volume**

Compare total trading volume between companies.

📈 **Yearly Performance**

Analyze average closing-price trends over time.

🔥 **Volatility Analysis**

Identify stocks with the highest average intraday volatility.

📉 **Daily Returns**

Analyze positive and negative price movements.

### Interactive Filters

- Ticker
- Year
- Quarter
- Month
- Date

---

# 📁 Recommended Repository Structure

```text
s&p500-data-warehouse/
│
├── data/
│   └── README.md
│
├── sql/
│   ├── 01_create_schemas.sql
│   ├── 02_create_staging.sql
│   ├── 03_create_dimensions.sql
│   ├── 04_create_fact.sql
│   ├── 05_etl.sql
│   ├── 06_data_quality.sql
│   ├── 07_audit_logging.sql
│   └── 08_analytics.sql
│
├── powerbi/
│   └── sp500_dashboard.pbix
│
├── docs/
│   ├── architecture.png
│   ├── star_schema.png
│   └── data_dictionary.md
│
├── screenshots/
│   └── dashboard.png
│
├── README.md
└── .gitignore
```

---

# 🚦 Project Status

| Component | Status |
|---|---|
| PostgreSQL setup | ✅ Complete |
| Raw dataset | ✅ Complete |
| Staging layer | ✅ Complete |
| Star Schema | ✅ Complete |
| Dimension tables | ✅ Complete |
| Fact table | ✅ Complete |
| ETL procedure | ✅ Complete |
| Data-quality checks | ✅ Complete |
| Duplicate protection | ✅ Complete |
| ETL audit logging | ✅ Complete |
| SQL analytics | 🔄 In progress |
| Power BI connection | 🔄 In progress |
| Power BI dashboard | ⏳ Planned |
| Incremental ETL | ⏳ Planned |
| Documentation | 🔄 In progress |
| Deployment | ⏳ Planned |

---

# 🧠 Key Data Warehousing Concepts Demonstrated

This project demonstrates practical understanding of:

- Data Warehouse Architecture
- Staging Layers
- ETL
- Star Schema
- Fact Tables
- Dimension Tables
- Surrogate Keys
- Foreign Keys
- Primary Keys
- Slowly evolving analytical structures
- Data Quality
- Data Validation
- Deduplication
- Idempotent Loads
- ETL Auditing
- SQL Aggregations
- Window Functions
- Time Dimensions
- Indexing
- Business Intelligence
- Power BI

---

# 🔮 Future Improvements

The next development stages include:

### 1. Incremental ETL

Instead of processing the complete dataset every time:

```text
New CSV
   ↓
Detect new records
   ↓
Load only new stock/date combinations
```

### 2. Advanced Analytics

Add:

- Moving averages
- Rolling returns
- Year-over-year performance
- Ranking functions
- Drawdown analysis
- Risk metrics
- Stock comparisons

### 3. Power BI Dashboard

Create a polished interactive dashboard with:

- KPI cards
- Stock selectors
- Time filters
- Price charts
- Volume charts
- Return analysis
- Volatility rankings

### 4. Production Improvements

Potential future additions:

- Docker
- Scheduled ETL
- Automated testing
- CI/CD
- Database monitoring
- Incremental pipelines
- Cloud deployment

---

# 💡 What This Project Demonstrates

This project is more than a collection of SQL queries.

It demonstrates the complete journey of analytical data:

```text
                 RAW DATA
                    │
                    ▼
              DATA INGESTION
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
             STAR SCHEMA
                    │
                    ▼
             DATA WAREHOUSE
                    │
                    ▼
             SQL ANALYTICS
                    │
                    ▼
               POWER BI
                    │
                    ▼
           BUSINESS INSIGHTS
```

The goal is to demonstrate how a data engineer can take **raw, unstructured source data and turn it into reliable, queryable, business-ready information**.

---

## 👨‍💻 Author

**Satish Kumar Peddi**

Built as a hands-on learning and portfolio project focused on:

- Data Engineering
- Data Warehousing
- SQL
- PostgreSQL
- ETL
- Business Intelligence
- Power BI

---

## ⭐ If You Find This Project Useful

Feel free to explore the SQL, data model, ETL pipeline, and Power BI dashboard.

If you're learning data warehousing yourself, the best way to use this project is to **build each layer rather than simply copying the final implementation**.

---

## 📌 Project Tagline

> **From raw stock-market data to a business-ready data warehouse.**
