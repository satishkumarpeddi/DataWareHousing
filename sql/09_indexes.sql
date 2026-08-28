CREATE INDEX IF NOT EXISTS idx_fact_date
ON warehouse.fact_stock_prices(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_company
ON warehouse.fact_stock_prices(company_key);

CREATE INDEX IF NOT EXISTS idx_company_ticker
ON warehouse.dim_company(ticker);

CREATE INDEX IF NOT EXISTS idx_date_full_date
ON warehouse.dim_date(full_date);