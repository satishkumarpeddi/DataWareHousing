-- ============================================================
-- Stock Volatility Analysis
-- Historical volatility based on daily returns
-- ============================================================

WITH price_data AS (
    SELECT
        c.company_key,
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
),

daily_returns AS (
    SELECT
        company_key,
        ticker,
        full_date,

        (
            (close_price - previous_close)
            / NULLIF(previous_close, 0)
        ) * 100 AS daily_return_percent

    FROM price_data
    WHERE previous_close IS NOT NULL
)

SELECT
    ticker,

    COUNT(*) AS trading_days,

    ROUND(
        STDDEV_SAMP(daily_return_percent)::numeric,
        4
    ) AS daily_volatility_percent,

    ROUND(
        (
            STDDEV_SAMP(daily_return_percent)
            * SQRT(252)
        )::numeric,
        4
    ) AS annualized_volatility_percent

FROM daily_returns

GROUP BY
    company_key,
    ticker

ORDER BY
    annualized_volatility_percent DESC;