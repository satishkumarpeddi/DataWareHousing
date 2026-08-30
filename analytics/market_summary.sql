-- ============================================================
-- Market Summary
-- ============================================================

SELECT
    d.year,

    d.month,

    d.month_name,

    COUNT(DISTINCT f.company_key)
        AS companies_traded,

    COUNT(*) AS total_stock_records,

    ROUND(AVG(f.close_price), 2)
        AS average_closing_price,

    ROUND(AVG(f.high_price), 2)
        AS average_high_price,

    ROUND(AVG(f.low_price), 2)
        AS average_low_price,

    SUM(f.volume)
        AS total_market_volume

FROM warehouse.fact_stock_prices f

JOIN warehouse.dim_date d
    ON f.date_key = d.date_key

GROUP BY
    d.year,
    d.month,
    d.month_name

ORDER BY
    d.year,
    d.month;