# Data Dictionary

## 1. Overview

This document describes the tables, columns, data types, constraints, and business meanings used in the S&P 500 Stock Data Warehouse.

The warehouse follows a **Star Schema** consisting of:

- `dim_date`
- `dim_company`
- `fact_stock_prices`

The project also contains staging and analytics layers.

---

# 2. Database Schemas

| Schema      | Purpose                                                 |
| ----------- | ------------------------------------------------------- |
| `staging`   | Temporary storage and data-quality processing           |
| `warehouse` | Dimension and fact tables used for analytical workloads |
| `analytics` | Views and queries used for analysis and reporting       |

---

# 3. Staging Layer

## 3.1 `staging.stock_prices`

This table stores stock-price data loaded from the source CSV before it is transformed and loaded into the warehouse.

| Column        | Data Type     | Nullable | Description                                       |
| ------------- | ------------- | -------: | ------------------------------------------------- |
| `date`        | DATE          |      Yes | Trading date                                      |
| `open_price`  | NUMERIC(18,6) |      Yes | Opening price of the stock                        |
| `high_price`  | NUMERIC(18,6) |      Yes | Highest price during the trading day              |
| `low_price`   | NUMERIC(18,6) |      Yes | Lowest price during the trading day               |
| `close_price` | NUMERIC(18,6) |      Yes | Closing price of the stock                        |
| `volume`      | BIGINT        |      Yes | Number of shares traded                           |
| `ticker`      | VARCHAR(20)   |      Yes | Stock ticker symbol                               |
| `loaded_at`   | TIMESTAMP     |       No | Timestamp when the record was loaded into staging |

### Source Example

```text
date        open_price  high_price  low_price  close_price  volume   ticker
2013-02-08  15.070000   15.120000   14.630000  14.750000    8407500  AAL
```

---

# 4. Data Quality Layer

## 4.1 `staging.data_quality_errors`

Stores records and information about data-quality problems identified during the ETL process.

| Column          | Data Type    | Nullable | Description                                         |
| --------------- | ------------ | -------: | --------------------------------------------------- |
| `error_id`      | BIGSERIAL    |       No | Unique identifier for the error                     |
| `load_id`       | BIGINT       |      Yes | Identifier of the ETL load that generated the error |
| `error_type`    | VARCHAR(100) |       No | Category of the data-quality error                  |
| `error_message` | TEXT         |       No | Detailed description of the error                   |
| `ticker`        | VARCHAR(20)  |      Yes | Stock ticker associated with the error              |
| `error_date`    | DATE         |      Yes | Trading date associated with the error              |
| `created_at`    | TIMESTAMP    |       No | Timestamp when the error was recorded               |

### Example Error Types

```text
NULL_STOCK_PRICE
INVALID_PRICE
NEGATIVE_VOLUME
DUPLICATE_RECORD
INVALID_DATE
MISSING_TICKER
```

---

# 5. ETL Metadata

## 5.1 `staging.load_metadata`

Stores information about each ETL execution.

| Column              | Data Type    | Nullable | Description                            |
| ------------------- | ------------ | -------: | -------------------------------------- |
| `load_id`           | BIGSERIAL    |       No | Unique identifier for an ETL load      |
| `source_file`       | VARCHAR(500) |      Yes | Name/path of the source file           |
| `load_start_time`   | TIMESTAMP    |       No | ETL start time                         |
| `load_end_time`     | TIMESTAMP    |      Yes | ETL completion time                    |
| `records_read`      | BIGINT       |      Yes | Number of records read from the source |
| `records_processed` | BIGINT       |      Yes | Number of records processed            |
| `records_inserted`  | BIGINT       |      Yes | Number of records inserted             |
| `records_updated`   | BIGINT       |      Yes | Number of records updated              |
| `records_rejected`  | BIGINT       |      Yes | Number of records rejected             |
| `status`            | VARCHAR(30)  |      Yes | Status of the ETL process              |
| `error_message`     | TEXT         |      Yes | Error information if the load fails    |

### Possible Status Values

```text
RUNNING
SUCCESS
FAILED
PARTIAL
```

---

# 6. Warehouse Layer

## 6.1 `warehouse.dim_date`

The date dimension provides calendar information used for time-based analysis.

| Column           | Data Type   | Nullable | Description                               |
| ---------------- | ----------- | -------: | ----------------------------------------- |
| `date_key`       | INTEGER     |       No | Surrogate/date key used by the fact table |
| `full_date`      | DATE        |       No | Complete calendar date                    |
| `day_number`     | INTEGER     |       No | Day of the month                          |
| `day_name`       | VARCHAR(20) |       No | Name of the day                           |
| `month_number`   | INTEGER     |       No | Month number from 1 to 12                 |
| `month_name`     | VARCHAR(20) |       No | Name of the month                         |
| `quarter_number` | INTEGER     |       No | Quarter from 1 to 4                       |
| `year_number`    | INTEGER     |       No | Calendar year                             |
| `day_of_week`    | INTEGER     |       No | Numeric day of week                       |
| `is_weekend`     | BOOLEAN     |       No | Indicates whether the date is a weekend   |

### Primary Key

```text
date_key
```

### Unique Key

```text
full_date
```

---

# 7. Company Dimension

## 7.1 `warehouse.dim_company`

Stores descriptive information about companies in the S&P 500 dataset.

| Column           | Data Type    | Nullable | Description                                     |
| ---------------- | ------------ | -------: | ----------------------------------------------- |
| `company_key`    | SERIAL       |       No | Surrogate key identifying the company           |
| `ticker`         | VARCHAR(20)  |       No | Stock ticker symbol                             |
| `company_name`   | VARCHAR(255) |      Yes | Full company name                               |
| `sector`         | VARCHAR(255) |      Yes | Business sector                                 |
| `industry`       | VARCHAR(255) |      Yes | Industry classification                         |
| `effective_date` | DATE         |       No | Date from which the record is effective         |
| `expiry_date`    | DATE         |      Yes | Date on which the record expires                |
| `is_current`     | BOOLEAN      |       No | Indicates whether the company record is current |

### Primary Key

```text
company_key
```

### Unique Constraint

```text
ticker
```

---

# 8. Fact Table

## 8.1 `warehouse.fact_stock_prices`

The fact table stores the measurable stock-market data used for analytical queries and reporting.

### Grain

> **One row represents one company's stock price information for one trading day.**

| Column        | Data Type     | Nullable | Description                        | Type        |
| ------------- | ------------- | -------: | ---------------------------------- | ----------- |
| `date_key`    | INTEGER       |       No | Reference to the date dimension    | Foreign Key |
| `company_key` | INTEGER       |       No | Reference to the company dimension | Foreign Key |
| `open_price`  | NUMERIC(18,6) |       No | Opening stock price                | Measure     |
| `high_price`  | NUMERIC(18,6) |       No | Highest stock price during the day | Measure     |
| `low_price`   | NUMERIC(18,6) |       No | Lowest stock price during the day  | Measure     |
| `close_price` | NUMERIC(18,6) |       No | Closing stock price                | Measure     |
| `volume`      | BIGINT        |       No | Number of shares traded            | Measure     |

### Primary Key

The fact table uses a composite primary key:

```text
(date_key, company_key)
```

This guarantees that a company cannot have multiple fact records for the same trading date.

### Foreign Keys

```text
date_key
    ↓
warehouse.dim_date(date_key)

company_key
    ↓
warehouse.dim_company(company_key)
```

---

# 9. Fact Table Data Quality Rules

The fact table contains several validation constraints.

## Open Price

```sql
open_price > 0
```

Opening prices must be positive.

## High Price

```sql
high_price > 0
```

The highest price must be positive.

## Low Price

```sql
low_price > 0
```

The lowest price must be positive.

## Close Price

```sql
close_price > 0
```

Closing prices must be positive.

## Volume

```sql
volume >= 0
```

Trading volume cannot be negative.

## High and Low

```sql
high_price >= low_price
```

The high price cannot be lower than the low price.

## High Price Relationship

```sql
high_price >= open_price
AND high_price >= close_price
```

The daily high must be at least as high as the opening and closing prices.

## Low Price Relationship

```sql
low_price <= open_price
AND low_price <= close_price
```

The daily low must be no greater than the opening and closing prices.

---

# 10. Analytics Layer

## 10.1 `analytics.stock_price_analysis`

This view combines the fact table with the date and company dimensions to provide analysis-ready stock data.

### Additional Calculated Measures

#### Daily Change

```sql
close_price - open_price
```

Represents the absolute price movement during the trading day.

#### Daily Return Percentage

```sql
((close_price - open_price) / open_price) * 100
```

Represents the percentage change between the opening and closing prices.

### View Columns

| Column                    | Description                       |
| ------------------------- | --------------------------------- |
| `full_date`               | Trading date                      |
| `day_name`                | Day of the week                   |
| `month_name`              | Month                             |
| `quarter_number`          | Quarter                           |
| `year_number`             | Year                              |
| `company_key`             | Company surrogate key             |
| `ticker`                  | Stock ticker                      |
| `company_name`            | Company name                      |
| `sector`                  | Company sector                    |
| `industry`                | Company industry                  |
| `open_price`              | Opening price                     |
| `high_price`              | Daily high                        |
| `low_price`               | Daily low                         |
| `close_price`             | Closing price                     |
| `volume`                  | Trading volume                    |
| `daily_change`            | Closing price minus opening price |
| `daily_return_percentage` | Percentage return                 |

---

# 11. Company Performance View

## 11.1 `analytics.company_performance`

Provides aggregated historical performance metrics for each company.

| Column                | Description                  |
| --------------------- | ---------------------------- |
| `ticker`              | Stock ticker                 |
| `company_name`        | Company name                 |
| `trading_days`        | Number of trading days       |
| `all_time_low`        | Lowest recorded stock price  |
| `all_time_high`       | Highest recorded stock price |
| `average_close_price` | Average closing price        |
| `total_volume`        | Total trading volume         |
| `first_trading_date`  | Earliest trading date        |
| `last_trading_date`   | Latest trading date          |

---

# 12. Relationships

The warehouse follows a Star Schema.

```text
                    ┌──────────────────┐
                    │    dim_date      │
                    │──────────────────│
                    │ PK date_key      │
                    │ full_date        │
                    │ day_name         │
                    │ month_name       │
                    │ quarter_number   │
                    │ year_number      │
                    └────────┬─────────┘
                             │
                             │
                             ▼
                    ┌─────────────────────┐
                    │ fact_stock_prices   │
                    │─────────────────────│
                    │ PK/FK date_key      │
                    │ PK/FK company_key   │
                    │ open_price          │
                    │ high_price          │
                    │ low_price           │
                    │ close_price         │
                    │ volume              │
                    └──────────┬──────────┘
                               │
                               │
                               ▼
                    ┌──────────────────┐
                    │   dim_company    │
                    │──────────────────│
                    │ PK company_key   │
                    │ ticker           │
                    │ company_name     │
                    │ sector           │
                    │ industry         │
                    └──────────────────┘
```

---

# 13. Data Flow

```text
Source CSV
    │
    ▼
Python / Pandas
    │
    ▼
staging.stock_prices
    │
    ▼
Data Quality Validation
    │
    ├──────────────► data_quality_errors
    │
    ▼
Dimension Tables
    │
    ├──────────────► dim_date
    │
    └──────────────► dim_company
    │
    ▼
fact_stock_prices
    │
    ▼
Analytics Views
    │
    ├──────────────► stock_price_analysis
    │
    └──────────────► company_performance
    │
    ▼
Power BI
```

---

# 14. Summary

The warehouse separates data into three major categories:

### Dimensions

Descriptive information used to filter and group data.

```text
dim_date
dim_company
```

### Facts

Numerical business measurements.

```text
open_price
high_price
low_price
close_price
volume
```

### Analytics

Calculated and aggregated information used for reporting.

```text
daily_change
daily_return_percentage
trading_days
all_time_low
all_time_high
average_close_price
total_volume
```

This design provides a structured foundation for historical stock analysis, SQL analytics, and Power BI reporting.
