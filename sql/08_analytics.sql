CREATE OR REPLACE VIEW analytics.stock_summary AS
SELECT
    c.ticker,
    COUNT(*) AS trading_days,
    ROUND(AVG(f.close_price), 2) AS avg_close_price,
    MAX(f.high_price) AS highest_price,
    MIN(f.low_price) AS lowest_price,
    SUM(f.volume) AS total_volume
FROM warehouse.fact_stock_prices f
JOIN warehouse.dim_company c
    ON f.company_key = c.company_key
GROUP BY c.ticker;


SELECT *
FROM analytics.stock_summary
ORDER BY total_volume DESC;