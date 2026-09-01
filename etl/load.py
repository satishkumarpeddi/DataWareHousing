"""
Load Clean Stock Data into PostgreSQL.

Pipeline:

CSV
 ↓
Extract
 ↓
Transform
 ↓
Validate
 ↓
Clean
 ↓
PostgreSQL staging.stock_prices
"""

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "DataWarehouse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")



CLEAN_DATA_FILE = Path(
    "data/processed/stocks_clean.csv"
)



def get_engine():
    """
    Create PostgreSQL SQLAlchemy engine.
    """

    if not DB_PASSWORD:
        raise ValueError(
            "DB_PASSWORD is not configured. "
            "Add DB_PASSWORD to your .env file."
        )

    connection_string = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/"
        f"{DB_NAME}"
    )

    engine = create_engine(
        connection_string,
        pool_pre_ping=True
    )

    return engine



def load_clean_csv():
    """
    Read the cleaned CSV file.
    """

    if not CLEAN_DATA_FILE.exists():

        raise FileNotFoundError(
            f"Clean data file not found: "
            f"{CLEAN_DATA_FILE}"
        )

    print(
        f"Reading clean data: "
        f"{CLEAN_DATA_FILE}"
    )

    df = pd.read_csv(
        CLEAN_DATA_FILE
    )

    print(
        f"Records read: {len(df):,}"
    )

    return df



def prepare_data(df):
    """
    Prepare cleaned data for PostgreSQL.
    """

    df = df.copy()


    required_columns = [
        "date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
        "ticker"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing columns: {missing_columns}"
        )


    df = df[
        required_columns
    ].copy()


    df["date"] = pd.to_datetime(
        df["date"],
        errors="raise"
    )


    numeric_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="raise"
        )


    df["ticker"] = (
        df["ticker"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return df



def validate_before_load(df):
    """
    Final safety checks before inserting into PostgreSQL.
    """

    print(
        "\nRunning final database-load validation..."
    )


    null_count = (
        df.isnull()
        .sum()
        .sum()
    )

    if null_count > 0:

        raise ValueError(
            f"Cannot load data containing "
            f"{null_count} NULL values."
        )

    price_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price"
    ]

    for column in price_columns:

        invalid_count = (
            df[column] <= 0
        ).sum()

        if invalid_count > 0:

            raise ValueError(
                f"{invalid_count} invalid values "
                f"found in {column}."
            )


    invalid_high_low = (
        df["high_price"] < df["low_price"]
    ).sum()

    if invalid_high_low > 0:

        raise ValueError(
            f"{invalid_high_low} records have "
            "high_price < low_price."
        )

    invalid_open = (
        (df["open_price"] < df["low_price"]) |
        (df["open_price"] > df["high_price"])
    ).sum()

    if invalid_open > 0:

        raise ValueError(
            f"{invalid_open} records have "
            "invalid open_price."
        )


    invalid_close = (
        (df["close_price"] < df["low_price"]) |
        (df["close_price"] > df["high_price"])
    ).sum()

    if invalid_close > 0:

        raise ValueError(
            f"{invalid_close} records have "
            "invalid close_price."
        )


    negative_volume = (
        df["volume"] < 0
    ).sum()

    if negative_volume > 0:

        raise ValueError(
            f"{negative_volume} records have "
            "negative volume."
        )


    empty_ticker = (
        df["ticker"]
        .astype(str)
        .str.strip()
        .eq("")
    ).sum()

    if empty_ticker > 0:

        raise ValueError(
            f"{empty_ticker} records have "
            "empty ticker values."
        )

    duplicate_count = df.duplicated(
        subset=["date", "ticker"]
    ).sum()

    if duplicate_count > 0:

        raise ValueError(
            f"{duplicate_count} duplicate "
            "date/ticker records found."
        )

    print(
        "✓ Final validation passed"
    )


def clear_staging_table(engine):
    """
    Clear existing staging records.

    This prevents duplicate data when the ETL
    pipeline is executed multiple times.
    """

    print(
        "\nClearing staging.stock_prices..."
    )

    with engine.begin() as connection:

        connection.execute(
            text(
                "TRUNCATE TABLE staging.stock_prices"
            )
        )

    print(
        "✓ staging.stock_prices cleared"
    )


def load_to_staging(df, engine):
    """
    Load clean records into staging.stock_prices.
    """

    print(
        "\nLoading data into "
        "staging.stock_prices..."
    )

    df.to_sql(
        name="stock_prices",
        con=engine,
        schema="staging",
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print(
        "✓ Data loaded into staging.stock_prices"
    )



def verify_load(df, engine):
    """
    Verify the number of records loaded.
    """

    query = text(
        """
        SELECT COUNT(*)
        FROM staging.stock_prices
        """
    )

    with engine.connect() as connection:

        database_count = connection.execute(
            query
        ).scalar()

    expected_count = len(df)

    print("\n=== LOAD VERIFICATION ===")

    print(
        f"Expected records : {expected_count:,}"
    )

    print(
        f"Database records : {database_count:,}"
    )

    if database_count != expected_count:

        raise ValueError(
            "Record count mismatch! "
            f"Expected {expected_count:,}, "
            f"found {database_count:,}."
        )

    print(
        "✓ Record count verification passed"
    )


def database_quality_check(engine):
    """
    Perform final quality checks directly
    against PostgreSQL.
    """

    print(
        "\n=== DATABASE QUALITY CHECK ==="
    )

    checks = {

        "NULL records": """
            SELECT COUNT(*)
            FROM staging.stock_prices
            WHERE date IS NULL
               OR open_price IS NULL
               OR high_price IS NULL
               OR low_price IS NULL
               OR close_price IS NULL
               OR volume IS NULL
               OR ticker IS NULL
        """,

        "High < Low": """
            SELECT COUNT(*)
            FROM staging.stock_prices
            WHERE high_price < low_price
        """,

        "Invalid Open": """
            SELECT COUNT(*)
            FROM staging.stock_prices
            WHERE open_price < low_price
               OR open_price > high_price
        """,

        "Invalid Close": """
            SELECT COUNT(*)
            FROM staging.stock_prices
            WHERE close_price < low_price
               OR close_price > high_price
        """,

        "Negative Volume": """
            SELECT COUNT(*)
            FROM staging.stock_prices
            WHERE volume < 0
        """
    }

    with engine.connect() as connection:

        for check_name, query in checks.items():

            result = connection.execute(
                text(query)
            )

            count = result.scalar()

            print(
                f"{check_name}: {count}"
            )

            if count != 0:

                raise ValueError(
                    f"Database quality check failed: "
                    f"{check_name}"
                )

    print(
        "\n✓ All database quality checks passed"
    )


if __name__ == "__main__":

    print(
        "======================================"
    )

    print(
        "      CLEAN DATA LOAD PIPELINE"
    )

    print(
        "======================================"
    )

    try:

        df = load_clean_csv()

        df = prepare_data(df)


        validate_before_load(df)


        engine = get_engine()

        print(
            "\n✓ PostgreSQL connection established"
        )


        clear_staging_table(
            engine
        )


        load_to_staging(
            df,
            engine
        )


        verify_load(
            df,
            engine
        )


        database_quality_check(
            engine
        )

        # -------------------------------------------------
        # Final result
        # -------------------------------------------------

        print(
            "\n======================================"
        )

        print(
            "      LOAD COMPLETED SUCCESSFULLY"
        )

        print(
            "======================================"
        )

    except Exception as error:

        print(
            "\n======================================"
        )

        print(
            "          LOAD FAILED"
        )

        print(
            "======================================"
        )

        print(
            f"Error: {error}"
        )

        raise