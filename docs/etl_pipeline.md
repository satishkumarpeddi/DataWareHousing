# ETL Pipeline

## 1. Overview

The S&P 500 Data Warehouse uses an ETL (Extract, Transform, Load) pipeline to move stock-market data from the raw CSV source into PostgreSQL.

The pipeline is designed to:

- Extract raw stock data
- Clean and transform the data
- Perform data-quality validation
- Load valid data into PostgreSQL staging
- Populate warehouse dimensions
- Load the fact table
- Record rejected records
- Track ETL execution metadata
- Log pipeline execution details

---

# 2. ETL Architecture

```text
                    Raw CSV
                       |
                       v
                ┌─────────────┐
                │  Extract    │
                │ extract.py  │
                └──────┬──────┘
                       |
                       v
                ┌─────────────┐
                │ Transform   │
                │transform.py │
                └──────┬──────┘
                       |
                       v
                ┌─────────────┐
                │  Validate   │
                │ validate.py │
                └──────┬──────┘
                       |
                ┌──────┴──────┐
                |             |
              VALID        INVALID
                |             |
                v             v
             Load          Error Log
                |             |
                v             v
       staging.stock_prices
                |
                v
        Warehouse Dimensions
          /             \
         v               v
    dim_date       dim_company
          \             /
           \           /
             v       v
          fact_stock_prices
                 |
                 v
             Analytics
                 |
                 v
              Power BI
```

---

# 3. ETL Directory Structure

```text
etl/
├── __init__.py
├── config.py
├── logger.py
├── extract.py
├── transform.py
├── validate.py
├── load.py
└── pipeline.py
```

---

# 4. Configuration

## `config.py`

The configuration module contains centralized settings used by the ETL pipeline.

Responsibilities include:

- Database configuration
- Raw data location
- Log directory
- PostgreSQL schema names
- Table names

Example:

```python
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "DataWarehouse"
DB_USER = "postgres"
```

Database credentials should preferably be loaded through environment variables or a `.env` file.

---

# 5. Logging

## `logger.py`

The logger records technical information about ETL execution.

The logging system records:

- Pipeline start
- Pipeline completion
- Extraction status
- Transformation status
- Validation status
- Loading status
- Warnings
- Errors
- Exceptions

Example log:

```text
2026-08-30 16:30:10 | INFO | ETL pipeline started
2026-08-30 16:30:11 | INFO | Extraction completed
2026-08-30 16:30:12 | INFO | Transformation completed
2026-08-30 16:30:13 | INFO | Validation completed
2026-08-30 16:30:14 | INFO | Warehouse load completed
2026-08-30 16:30:14 | INFO | ETL pipeline completed successfully
```

---

# 6. Extract

## `extract.py`

The extraction stage reads the raw S&P 500 CSV file into a Pandas DataFrame.

### Input

```text
data/data/processed
```

### Output

```text
Pandas DataFrame
```

Typical source columns:

```text
date
open
high
low
close
volume
Name
```

The extraction stage does not perform major transformations. Its primary responsibility is retrieving the source data.

---

# 7. Transform

## `transform.py`

The transformation stage cleans and standardizes the extracted data.

### Main transformations

#### Column standardization

Source column names are converted into consistent names.

```text
open  → open_price
high  → high_price
low   → low_price
close → close_price
Name  → ticker
```

#### Date conversion

```python
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)
```

#### Numeric conversion

Price and volume columns are converted into numeric data types.

```text
open_price
high_price
low_price
close_price
volume
```

#### Ticker normalization

Ticker symbols are trimmed and converted to uppercase.

```text
" aapl " → "AAPL"
```

---

# 8. Validation

## `validate.py`

The validation stage checks the transformed dataset before it is loaded into the warehouse.

## 8.1 NULL Validation

The following fields must contain valid values before entering the fact table:

```text
open_price
high_price
low_price
close_price
volume
```

Example:

```sql
WHERE open_price IS NULL
   OR high_price IS NULL
   OR low_price IS NULL
   OR close_price IS NULL
   OR volume IS NULL
```

Invalid records are rejected and recorded in:

```text
staging.data_quality_errors
```

---

# 9. Price Validation

Stock prices must satisfy the following rules:

```text
open_price  > 0
high_price  > 0
low_price   > 0
close_price > 0
```

The following relationship must also hold:

```text
high_price >= low_price
```

And:

```text
high_price >= open_price
high_price >= close_price
```

And:

```text
low_price <= open_price
low_price <= close_price
```

These rules protect the warehouse from invalid financial data.

---

# 10. Volume Validation

Trading volume cannot be negative.

```text
volume >= 0
```

Records containing negative volume values are rejected.

---

# 11. Duplicate Validation

The intended grain of the fact table is:

> One company for one trading date.

Therefore:

```text
date + ticker
```

must be unique in the staging data.

Duplicate records are detected before loading.

Example:

```sql
SELECT
    date,
    ticker,
    COUNT(*)
FROM staging.stock_prices
GROUP BY date, ticker
HAVING COUNT(*) > 1;
```

---

# 12. Staging Load

After validation, valid records are loaded into:

```text
staging.stock_prices
```

The staging layer provides a temporary and controlled area before the data enters the dimensional warehouse.

---

# 13. Dimension Loading

The warehouse contains two primary dimensions.

## Date Dimension

```text
warehouse.dim_date
```

The ETL process maps the trading date to:

```text
date_key
```

## Company Dimension

```text
warehouse.dim_company
```

The ETL process maps the ticker symbol to:

```text
company_key
```

These surrogate keys are then used by the fact table.

---

# 14. Fact Loading

## `fact_stock_prices`

The fact table receives the validated stock measurements.

```text
date_key
company_key
open_price
high_price
low_price
close_price
volume
```

The fact table uses:

```sql
PRIMARY KEY (date_key, company_key)
```

This represents the grain:

> One company's stock information for one trading day.

---

# 15. Fact Loading Process

The fact table is populated by joining staging data with the dimension tables.

```sql
INSERT INTO warehouse.fact_stock_prices (
    date_key,
    company_key,
    open_price,
    high_price,
    low_price,
    close_price,
    volume
)
SELECT
    d.date_key,
    c.company_key,
    s.open_price,
    s.high_price,
    s.low_price,
    s.close_price,
    s.volume
FROM staging.stock_prices s
JOIN warehouse.dim_date d
    ON s.date = d.full_date
JOIN warehouse.dim_company c
    ON s.ticker = c.ticker
ON CONFLICT (date_key, company_key)
DO NOTHING;
```

---

# 16. Data Quality Error Handling

Invalid records are stored in:

```text
staging.data_quality_errors
```

Examples include:

```text
NULL_STOCK_PRICE
INVALID_PRICE
NEGATIVE_VOLUME
DUPLICATE_RECORD
INVALID_DATE
MISSING_TICKER
```

This allows invalid data to be investigated without contaminating the warehouse.

---

# 17. ETL Load Metadata

Every ETL execution can be tracked using:

```text
staging.load_metadata
```

Important metrics include:

```text
records_read
records_processed
records_inserted
records_updated
records_rejected
load_start_time
load_end_time
status
```

This provides operational visibility into the ETL process.

---

# 18. Pipeline Orchestration

## `pipeline.py`

The pipeline module coordinates all ETL components.

The execution sequence is:

```text
1. Initialize configuration
        |
        v
2. Initialize logger
        |
        v
3. Extract data
        |
        v
4. Transform data
        |
        v
5. Validate data
        |
        v
6. Load staging data
        |
        v
7. Load dimensions
        |
        v
8. Load fact table
        |
        v
9. Update load metadata
        |
        v
10. Complete ETL
```

---

# 19. Error Handling

The pipeline uses exception handling to prevent silent failures.

Example:

```python
try:

    # ETL process

except Exception as e:

    logger.exception(
        "ETL pipeline failed: %s",
        e
    )

    raise
```

When an unexpected error occurs:

1. The error is written to the log.
2. The ETL process is stopped.
3. The failure can be investigated.
4. Load metadata can be updated with the failure status.

---

# 20. ETL Monitoring

The ETL process can be monitored using both logs and database metadata.

```text
             ETL Monitoring
                   |
          ┌────────┴────────┐
          |                 |
          v                 v
       logger.py      load_metadata
          |                 |
          v                 v
     Technical logs    ETL statistics
```

### Logs

Used for:

- Debugging
- Exceptions
- Execution tracing
- Warnings

### Load Metadata

Used for:

- Record counts
- Load duration
- Insert counts
- Rejected records
- ETL status

---

# 21. Complete Data Flow

```text
                   S&P 500 CSV
                        |
                        v
                   extract.py
                        |
                        v
                  Pandas DataFrame
                        |
                        v
                  transform.py
                        |
                        v
                  validate.py
                    /       \
                   /         \
              VALID          INVALID
                |                |
                v                v
             load.py       data_quality_errors
                |
                v
        staging.stock_prices
                |
                v
        ┌───────┴────────┐
        |                |
        v                v
    dim_date        dim_company
        |                |
        └───────┬────────┘
                |
                v
        fact_stock_prices
                |
                v
             analytics
                |
                v
             Power BI
```

---

# 22. ETL Success Criteria

An ETL execution is considered successful when:

- Source data is successfully extracted.
- Required transformations are completed.
- Data-quality rules pass.
- Valid records are loaded into staging.
- Required dimension keys exist.
- Fact records are successfully inserted.
- Duplicate fact records are prevented.
- Rejected records are logged.
- Load metadata is updated.
- No unexpected exceptions occur.

---

# 23. Future Improvements

The ETL pipeline can be enhanced with:

- Incremental loading
- Batch processing
- Parallel processing
- Automated scheduling
- Retry mechanisms
- Email/notification alerts
- Data-quality dashboards
- ETL performance monitoring
- Docker deployment
- CI/CD automation
- Automated unit and integration tests

---

# 24. Summary

The ETL pipeline provides a controlled path from raw S&P 500 stock data to an analytical data warehouse.

```text
Extract
   ↓
Transform
   ↓
Validate
   ↓
Stage
   ↓
Dimensions
   ↓
Fact
   ↓
Analytics
   ↓
Power BI
```

The separation of extraction, transformation, validation, loading, configuration, and logging makes the pipeline modular, maintainable, testable, and easier to extend.
