DROP TABLE IF EXISTS staging.stocks_raw;

CREATE TABLE staging.stocks_raw (
    date DATE,
    open NUMERIC(18,4),
    high NUMERIC(18,4),
    low NUMERIC(18,4),
    close NUMERIC(18,4),
    volume BIGINT,
    name VARCHAR(20)
);