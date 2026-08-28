-- ============================================================
-- Company Performance
-- ============================================================

SELECT
    c.ticker,

    COUNT(*) AS trading_days,

    ROUND(AVG(f.close_price), 2) AS average_close_price,

    ROUND(MIN(f.low_price), 2) AS minimum_price,

    ROUND(MAX(f.high_price), 2) AS maximum_price,

    SUM(f.volume) AS total_trading_volume,

    ROUND(AVG(f.high_price - f.low_price), 2)
        AS average_daily_range,

    ROUND(
        (
            (
                MAX(d.full_date)
            )
        )::numeric,
        0
    ) AS analysis_period

FROM warehouse.fact_stock_prices f

JOIN warehouse.dim_company c
    ON f.company_key = c.company_key

JOIN warehouse.dim_date d
    ON f.date_key = d.date_key

GROUP BY c.ticker

ORDER BY total_trading_volume DESC;