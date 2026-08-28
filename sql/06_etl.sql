CREATE OR REPLACE PROCEDURE warehouse.load_stock_data()
LANGUAGE plpgsql
AS $$
BEGIN

    INSERT INTO warehouse.fact_stock_prices (
        date_key,
        company_key,
        open_price,
        high_price,
        low_price,
        close_price,
        volume
    )
    SELECT
        d.date_key,
        c.company_key,
        s.open,
        s.high,
        s.low,
        s.close,
        s.volume
    FROM staging.stocks_raw s
    JOIN warehouse.dim_date d
        ON d.full_date = s.date
    JOIN warehouse.dim_company c
        ON c.ticker = s.name
    ON CONFLICT (date_key, company_key)
    DO UPDATE SET
        open_price = EXCLUDED.open_price,
        high_price = EXCLUDED.high_price,
        low_price = EXCLUDED.low_price,
        close_price = EXCLUDED.close_price,
        volume = EXCLUDED.volume;

END;
$$;

CALL warehouse.load_stock_data();