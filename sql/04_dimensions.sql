CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    day INTEGER,
    day_name VARCHAR(20),
    week_of_year INTEGER
);


CREATE TABLE IF NOT EXISTS warehouse.dim_company (
    company_key SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL UNIQUE
);