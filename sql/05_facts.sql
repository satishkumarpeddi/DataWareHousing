CREATE TABLE IF NOT EXISTS warehouse.fact_stock_prices (
    stock_price_key BIGSERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL,
    company_key INTEGER NOT NULL,
    open_price NUMERIC(18,4),
    high_price NUMERIC(18,4),
    low_price NUMERIC(18,4),
    close_price NUMERIC(18,4),
    volume BIGINT,

    CONSTRAINT fk_fact_date
        FOREIGN KEY (date_key)
        REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT fk_fact_company
        FOREIGN KEY (company_key)
        REFERENCES warehouse.dim_company(company_key),

    CONSTRAINT uq_fact_stock
        UNIQUE (date_key, company_key)
);