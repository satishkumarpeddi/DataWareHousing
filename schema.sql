-- Create The Schemas


CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Staging Schema

CREATE TABLE IF NOT EXISTS staging.stock_prices (
    date DATE,
    open_price NUMERIC(18,6),
    high_price NUMERIC(18,6),
    low_price NUMERIC(18,6),
    close_price NUMERIC(18,6),
    volume BIGINT,
    ticker VARCHAR(20),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data quality error table

CREATE TABLE IF NOT EXISTS staging.data_quality_errors (
    error_id BIGSERIAL PRIMARY KEY,
    load_id BIGINT,
    error_type VARCHAR(100) NOT NULL,
    error_message TEXT NOT NULL,
    ticker VARCHAR(20),
    error_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ETL load metadata

CREATE TABLE IF NOT EXISTS staging.load_metadata (
    load_id BIGSERIAL PRIMARY KEY,
    source_file VARCHAR(500),
    load_start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    load_end_time TIMESTAMP,
    records_read BIGINT DEFAULT 0,
    records_processed BIGINT DEFAULT 0,
    records_inserted BIGINT DEFAULT 0,
    records_updated BIGINT DEFAULT 0,
    records_rejected BIGINT DEFAULT 0,
    status VARCHAR(30) DEFAULT 'RUNNING',
    error_message TEXT
);

-- Warehouse schema

                    dim_date
                       │
                       │
                       ▼
dim_company ───► fact_stock_prices

-- Date Dimension


CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_number INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    month_number INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter_number INTEGER NOT NULL,
    year_number INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

-- Company Dimension

CREATE TABLE IF NOT EXISTS warehouse.dim_company (
    company_key SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    company_name VARCHAR(255),
    sector VARCHAR(255),
    industry VARCHAR(255),
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    expiry_date DATE,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_dim_company_ticker
        UNIQUE (ticker)
);

-- Fact Table

CREATE TABLE IF NOT EXISTS warehouse.fact_stock_prices (
    date_key INTEGER NOT NULL,
    company_key INTEGER NOT NULL,

    open_price NUMERIC(18,6) NOT NULL,
    high_price NUMERIC(18,6) NOT NULL,
    low_price NUMERIC(18,6) NOT NULL,
    close_price NUMERIC(18,6) NOT NULL,
    volume BIGINT NOT NULL,

    CONSTRAINT pk_fact_stock_prices
        PRIMARY KEY (date_key, company_key),

    CONSTRAINT fk_fact_date
        FOREIGN KEY (date_key)
        REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT fk_fact_company
        FOREIGN KEY (company_key)
        REFERENCES warehouse.dim_company(company_key),

    CONSTRAINT chk_open_positive
        CHECK (open_price > 0),

    CONSTRAINT chk_high_positive
        CHECK (high_price > 0),

    CONSTRAINT chk_low_positive
        CHECK (low_price > 0),

    CONSTRAINT chk_close_positive
        CHECK (close_price > 0),

    CONSTRAINT chk_volume_nonnegative
        CHECK (volume >= 0),

    CONSTRAINT chk_high_low
        CHECK (high_price >= low_price),

    CONSTRAINT chk_high_open_close
        CHECK (
            high_price >= open_price
            AND high_price >= close_price
        ),

    CONSTRAINT chk_low_open_close
        CHECK (
            low_price <= open_price
            AND low_price <= close_price
        )
);


-- Indexes

CREATE INDEX IF NOT EXISTS idx_fact_company
ON warehouse.fact_stock_prices(company_key);

CREATE INDEX IF NOT EXISTS idx_fact_date
ON warehouse.fact_stock_prices(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_company_date
ON warehouse.fact_stock_prices(company_key, date_key);


-- Analytics Schema

CREATE OR REPLACE VIEW analytics.stock_price_analysis AS
SELECT
    d.full_date,
    d.day_name,
    d.month_name,
    d.quarter_number,
    d.year_number,

    c.company_key,
    c.ticker,
    c.company_name,
    c.sector,
    c.industry,

    f.open_price,
    f.high_price,
    f.low_price,
    f.close_price,
    f.volume,

    f.close_price - f.open_price AS daily_change,

    CASE
        WHEN f.open_price <> 0
        THEN ((f.close_price - f.open_price) / f.open_price) * 100
        ELSE NULL
    END AS daily_return_percentage

FROM warehouse.fact_stock_prices f

JOIN warehouse.dim_date d
    ON f.date_key = d.date_key

JOIN warehouse.dim_company c
    ON f.company_key = c.company_key;


-- Create a KPI View

CREATE OR REPLACE VIEW analytics.company_performance AS
SELECT
    c.ticker,
    c.company_name,

    COUNT(*) AS trading_days,

    MIN(f.low_price) AS all_time_low,

    MAX(f.high_price) AS all_time_high,

    AVG(f.close_price) AS average_close_price,

    SUM(f.volume) AS total_volume,

    MIN(d.full_date) AS first_trading_date,

    MAX(d.full_date) AS last_trading_date

FROM warehouse.fact_stock_prices f

JOIN warehouse.dim_company c
    ON f.company_key = c.company_key

JOIN warehouse.dim_date d
    ON f.date_key = d.date_key

GROUP BY
    c.ticker,
    c.company_name;



