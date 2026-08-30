-- ============================================================
-- Monthly Stock Performance
-- ============================================================

WITH monthly_prices AS (
    SELECT
        c.ticker,
        d.year,
        d.month,
        d.month_name,
        MIN(d.full_date) AS first_trading_date,
        MAX(d.full_date) AS last_trading_date,

        FIRST_VALUE(f.close_price) OVER (
            PARTITION BY c.company_key, d.year, d.month
            ORDER BY d.full_date
        ) AS opening_month_price,

        LAST_VALUE(f.close_price) OVER (
            PARTITION BY c.company_key, d.year, d.month
            ORDER BY d.full_date
            ROWS BETWEEN UNBOUNDED PRECEDING
                 AND UNBOUNDED FOLLOWING
        ) AS closing_month_price,

        SUM(f.volume) OVER (
            PARTITION BY c.company_key, d.year, d.month
        ) AS monthly_volume

    FROM warehouse.fact_stock_prices f

    JOIN warehouse.dim_company c
        ON f.company_key = c.company_key

    JOIN warehouse.dim_date d
        ON f.date_key = d.date_key
)

SELECT DISTINCT
    ticker,
    year,
    month,
    month_name,
    first_trading_date,
    last_trading_date,
    opening_month_price,
    closing_month_price,
    monthly_volume,

    ROUND(
        (
            (closing_month_price - opening_month_price)
            / NULLIF(opening_month_price, 0)
        ) * 100,
        4
    ) AS monthly_return_percent

FROM monthly_prices
ORDER BY ticker, year, month;