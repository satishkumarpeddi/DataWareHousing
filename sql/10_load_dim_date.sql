-- =====================================================
-- LOAD DIM_DATE
-- =====================================================

INSERT INTO warehouse.dim_date
(
    date_key,
    full_date,
    day,
    month,
    month_name,
    quarter,
    year,
    day_of_week,
    day_name
)
SELECT DISTINCT
    TO_CHAR(date, 'YYYYMMDD')::INTEGER AS date_key,
    date::DATE AS full_date,
    EXTRACT(DAY FROM date)::INTEGER AS day,
    EXTRACT(MONTH FROM date)::INTEGER AS month,
    TO_CHAR(date, 'Month') AS month_name,
    EXTRACT(QUARTER FROM date)::INTEGER AS quarter,
    EXTRACT(YEAR FROM date)::INTEGER AS year,
    EXTRACT(ISODOW FROM date)::INTEGER AS day_of_week,
    TO_CHAR(date, 'Day') AS day_name
FROM staging.stock_prices
WHERE date IS NOT NULL
ON CONFLICT (date_key) DO NOTHING;