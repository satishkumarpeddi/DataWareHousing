-- ============================================================
-- Daily Stock Returns
-- ============================================================

WITH price_data AS (
    SELECT
        c.ticker,
        d.full_date,
        f.close_price,

        LAG(f.close_price) OVER (
            PARTITION BY c.company_key
            ORDER BY d.full_date
        ) AS previous_close

    FROM warehouse.fact_stock_prices f

    JOIN warehouse.dim_company c
        ON f.company_key = c.company_key

    JOIN warehouse.dim_date d
        ON f.date_key = d.date_key
)

SELECT
    ticker,
    full_date,
    close_price,
    previous_close,

    ROUND(
        ((close_price - previous_close)
        / NULLIF(previous_close, 0)) * 100,
        4
    ) AS daily_return_percent

FROM price_data
WHERE previous_close IS NOT NULL
ORDER BY ticker, full_date;