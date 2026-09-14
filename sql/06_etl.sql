CREATE OR REPLACE PROCEDURE warehouse.load_stock_data()
LANGUAGE plpgsql
AS $$
BEGIN

    -- Quarantine invalid OHLC rows
    INSERT INTO staging.data_quality_errors (
        error_type,
        error_message,
        ticker,
        error_date
    )
    SELECT
        'INVALID_OHLC',
        CASE
            WHEN high_price < low_price
                THEN 'high_price is less than low_price'
            WHEN open_price < low_price OR open_price > high_price
                THEN 'open_price is outside high/low range'
            WHEN close_price < low_price OR close_price > high_price
                THEN 'close_price is outside high/low range'
            ELSE 'Invalid OHLC values'
        END,
        ticker,
        date
    FROM staging.stock_prices
    WHERE high_price < low_price
       OR open_price < low_price
       OR open_price > high_price
       OR close_price < low_price
       OR close_price > high_price;


    -- Load only valid records into the fact table
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
        s.open_price,
        s.high_price,
        s.low_price,
        s.close_price,
        s.volume
    FROM staging.stock_prices s
    JOIN warehouse.dim_date d
        ON d.full_date = s.date
    JOIN warehouse.dim_company c
        ON c.ticker = s.ticker
    WHERE s.high_price >= s.low_price
      AND s.open_price BETWEEN s.low_price AND s.high_price
      AND s.close_price BETWEEN s.low_price AND s.high_price

    ON CONFLICT (date_key, company_key)
    DO UPDATE SET
        open_price = EXCLUDED.open_price,
        high_price = EXCLUDED.high_price,
        low_price = EXCLUDED.low_price,
        close_price = EXCLUDED.close_price,
        volume = EXCLUDED.volume;

END;
$$;
