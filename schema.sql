--
-- PostgreSQL database dump
--

\restrict bmfJfBNCp7qC1ktiNUd9hslgfFhZfitKG7TicSUj9kgkbNvtwVmJ0o5IVju5boc

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: staging; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA staging;


ALTER SCHEMA staging OWNER TO postgres;

--
-- Name: warehouse; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA warehouse;


ALTER SCHEMA warehouse OWNER TO postgres;

--
-- Name: load_stock_data(); Type: PROCEDURE; Schema: warehouse; Owner: postgres
--

CREATE PROCEDURE warehouse.load_stock_data()
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_audit_id BIGINT;
    v_start_time TIMESTAMP;
    v_rows_loaded BIGINT;
BEGIN

    v_start_time := CURRENT_TIMESTAMP;

    -- Start audit record
    INSERT INTO warehouse.etl_audit (
        process_name,
        start_time,
        status
    )
    VALUES (
        'load_stock_data',
        v_start_time,
        'RUNNING'
    )
    RETURNING audit_id INTO v_audit_id;


    -- ==========================================
    -- 1. Load Company Dimension
    -- ==========================================

    INSERT INTO warehouse.dim_company (ticker)
    SELECT DISTINCT ticker
    FROM staging.stock_prices
    WHERE ticker IS NOT NULL
    ON CONFLICT (ticker) DO NOTHING;


    -- ==========================================
    -- 2. Load Date Dimension
    -- ==========================================

    INSERT INTO warehouse.dim_date (
        date_key,
        full_date,
        year,
        quarter,
        month,
        month_name,
        day,
        day_name,
        week_of_year
    )
    SELECT DISTINCT
        TO_CHAR(date, 'YYYYMMDD')::INTEGER, --Type Casting
        date,
        EXTRACT(YEAR FROM date)::INTEGER,
        EXTRACT(QUARTER FROM date)::INTEGER,
        EXTRACT(MONTH FROM date)::INTEGER,
        TRIM(TO_CHAR(date, 'Month')),
        EXTRACT(DAY FROM date)::INTEGER,
        TRIM(TO_CHAR(date, 'Day')),
        EXTRACT(WEEK FROM date)::INTEGER
    FROM staging.stock_prices
    WHERE date IS NOT NULL
    ON CONFLICT (date_key) DO NOTHING;


    -- ==========================================
    -- 3. Load Fact Table
    -- ==========================================

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
        ON s.date = d.full_date
    JOIN warehouse.dim_company c
        ON s.ticker = c.ticker
    ON CONFLICT (date_key, company_key)
    DO NOTHING;


    -- Number of records currently in fact table
    SELECT COUNT(*)
    INTO v_rows_loaded
    FROM warehouse.fact_stock_prices;


    -- Successful audit
    UPDATE warehouse.etl_audit
    SET
        end_time = CURRENT_TIMESTAMP,
        status = 'SUCCESS',
        rows_loaded = v_rows_loaded
    WHERE audit_id = v_audit_id;


EXCEPTION
    WHEN OTHERS THEN

        UPDATE warehouse.etl_audit
        SET
            end_time = CURRENT_TIMESTAMP,
            status = 'FAILED',
            error_message = SQLERRM
        WHERE audit_id = v_audit_id;

        RAISE;

END;
$$;


ALTER PROCEDURE warehouse.load_stock_data() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: stock_prices; Type: TABLE; Schema: staging; Owner: postgres
--

CREATE TABLE staging.stock_prices (
    date date,
    open_price numeric(12,4),
    high_price numeric(12,4),
    low_price numeric(12,4),
    close_price numeric(12,4),
    volume bigint,
    ticker character varying(20)
);


ALTER TABLE staging.stock_prices OWNER TO postgres;

--
-- Name: dim_company; Type: TABLE; Schema: warehouse; Owner: postgres
--

CREATE TABLE warehouse.dim_company (
    company_key integer NOT NULL,
    ticker character varying(10) NOT NULL
);


ALTER TABLE warehouse.dim_company OWNER TO postgres;

--
-- Name: dim_company_company_key_seq; Type: SEQUENCE; Schema: warehouse; Owner: postgres
--

CREATE SEQUENCE warehouse.dim_company_company_key_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE warehouse.dim_company_company_key_seq OWNER TO postgres;

--
-- Name: dim_company_company_key_seq; Type: SEQUENCE OWNED BY; Schema: warehouse; Owner: postgres
--

ALTER SEQUENCE warehouse.dim_company_company_key_seq OWNED BY warehouse.dim_company.company_key;


--
-- Name: dim_date; Type: TABLE; Schema: warehouse; Owner: postgres
--

CREATE TABLE warehouse.dim_date (
    date_key integer NOT NULL,
    full_date date NOT NULL,
    year integer,
    quarter integer,
    month integer,
    month_name character varying(20),
    day integer,
    day_name character varying(20),
    week_of_year integer
);


ALTER TABLE warehouse.dim_date OWNER TO postgres;

--
-- Name: etl_audit; Type: TABLE; Schema: warehouse; Owner: postgres
--

CREATE TABLE warehouse.etl_audit (
    audit_id bigint NOT NULL,
    process_name character varying(100) NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone,
    status character varying(20) NOT NULL,
    rows_loaded bigint DEFAULT 0,
    error_message text
);


ALTER TABLE warehouse.etl_audit OWNER TO postgres;

--
-- Name: etl_audit_audit_id_seq; Type: SEQUENCE; Schema: warehouse; Owner: postgres
--

CREATE SEQUENCE warehouse.etl_audit_audit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE warehouse.etl_audit_audit_id_seq OWNER TO postgres;

--
-- Name: etl_audit_audit_id_seq; Type: SEQUENCE OWNED BY; Schema: warehouse; Owner: postgres
--

ALTER SEQUENCE warehouse.etl_audit_audit_id_seq OWNED BY warehouse.etl_audit.audit_id;


--
-- Name: fact_stock_prices; Type: TABLE; Schema: warehouse; Owner: postgres
--

CREATE TABLE warehouse.fact_stock_prices (
    stock_price_key bigint NOT NULL,
    date_key integer NOT NULL,
    company_key integer NOT NULL,
    open_price numeric(12,4),
    high_price numeric(12,4),
    low_price numeric(12,4),
    close_price numeric(12,4),
    volume bigint
);


ALTER TABLE warehouse.fact_stock_prices OWNER TO postgres;

--
-- Name: fact_stock_prices_stock_price_key_seq; Type: SEQUENCE; Schema: warehouse; Owner: postgres
--

CREATE SEQUENCE warehouse.fact_stock_prices_stock_price_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE warehouse.fact_stock_prices_stock_price_key_seq OWNER TO postgres;

--
-- Name: fact_stock_prices_stock_price_key_seq; Type: SEQUENCE OWNED BY; Schema: warehouse; Owner: postgres
--

ALTER SEQUENCE warehouse.fact_stock_prices_stock_price_key_seq OWNED BY warehouse.fact_stock_prices.stock_price_key;


--
-- Name: dim_company company_key; Type: DEFAULT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.dim_company ALTER COLUMN company_key SET DEFAULT nextval('warehouse.dim_company_company_key_seq'::regclass);


--
-- Name: etl_audit audit_id; Type: DEFAULT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.etl_audit ALTER COLUMN audit_id SET DEFAULT nextval('warehouse.etl_audit_audit_id_seq'::regclass);


--
-- Name: fact_stock_prices stock_price_key; Type: DEFAULT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.fact_stock_prices ALTER COLUMN stock_price_key SET DEFAULT nextval('warehouse.fact_stock_prices_stock_price_key_seq'::regclass);


--
-- Name: dim_company dim_company_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.dim_company
    ADD CONSTRAINT dim_company_pkey PRIMARY KEY (company_key);


--
-- Name: dim_company dim_company_ticker_key; Type: CONSTRAINT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.dim_company
    ADD CONSTRAINT dim_company_ticker_key UNIQUE (ticker);


--
-- Name: dim_date dim_date_full_date_key; Type: CONSTRAINT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.dim_date
    ADD CONSTRAINT dim_date_full_date_key UNIQUE (full_date);


--
-- Name: dim_date dim_date_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.dim_date
    ADD CONSTRAINT dim_date_pkey PRIMARY KEY (date_key);


--
-- Name: etl_audit etl_audit_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.etl_audit
    ADD CONSTRAINT etl_audit_pkey PRIMARY KEY (audit_id);


--
-- Name: fact_stock_prices fact_stock_prices_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.fact_stock_prices
    ADD CONSTRAINT fact_stock_prices_pkey PRIMARY KEY (stock_price_key);


--
-- Name: fact_stock_prices unique_stock_date; Type: CONSTRAINT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.fact_stock_prices
    ADD CONSTRAINT unique_stock_date UNIQUE (date_key, company_key);


--
-- Name: idx_dim_company_ticker; Type: INDEX; Schema: warehouse; Owner: postgres
--

CREATE INDEX idx_dim_company_ticker ON warehouse.dim_company USING btree (ticker);


--
-- Name: idx_fact_company; Type: INDEX; Schema: warehouse; Owner: postgres
--

CREATE INDEX idx_fact_company ON warehouse.fact_stock_prices USING btree (company_key);


--
-- Name: idx_fact_date; Type: INDEX; Schema: warehouse; Owner: postgres
--

CREATE INDEX idx_fact_date ON warehouse.fact_stock_prices USING btree (date_key);


--
-- Name: idx_fact_date_company; Type: INDEX; Schema: warehouse; Owner: postgres
--

CREATE INDEX idx_fact_date_company ON warehouse.fact_stock_prices USING btree (date_key, company_key);


--
-- Name: fact_stock_prices fk_fact_company; Type: FK CONSTRAINT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.fact_stock_prices
    ADD CONSTRAINT fk_fact_company FOREIGN KEY (company_key) REFERENCES warehouse.dim_company(company_key);


--
-- Name: fact_stock_prices fk_fact_date; Type: FK CONSTRAINT; Schema: warehouse; Owner: postgres
--

ALTER TABLE ONLY warehouse.fact_stock_prices
    ADD CONSTRAINT fk_fact_date FOREIGN KEY (date_key) REFERENCES warehouse.dim_date(date_key);


--
-- PostgreSQL database dump complete
--

\unrestrict bmfJfBNCp7qC1ktiNUd9hslgfFhZfitKG7TicSUj9kgkbNvtwVmJ0o5IVju5boc

