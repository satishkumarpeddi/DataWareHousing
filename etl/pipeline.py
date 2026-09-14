import os

from etl.extract import extract_data
from etl.transform import transform_data
from etl.validate import validate_data

from sqlalchemy import create_engine, text


def get_database_engine():
    """Create a PostgreSQL SQLAlchemy engine."""

    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "DataWarehouse")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD")

    if not db_password:
        raise ValueError("DB_PASSWORD is not configured")

    connection_string = (
        f"postgresql+psycopg2://"
        f"{db_user}:{db_password}@"
        f"{db_host}:{db_port}/{db_name}"
    )

    return create_engine(
        connection_string,
        pool_pre_ping=True
    )


def load_to_postgresql(df, engine):
    """Load transformed data into staging and update warehouse."""

    print("\nConnecting to PostgreSQL...")

    with engine.begin() as connection:

        connection.execute(
            text("TRUNCATE TABLE staging.stock_prices")
        )

    print("✓ staging.stock_prices cleared")

    print("Loading data into staging.stock_prices...")

    df.to_sql(
        name="stock_prices",
        con=engine,
        schema="staging",
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print(f"✓ Loaded {len(df):,} records into staging")

    print("Running warehouse.load_stock_data()...")

    with engine.begin() as connection:
        connection.execute(
            text("CALL warehouse.load_stock_data()")
        )

    print("✓ Warehouse load completed")


def verify_warehouse(engine):
    """Verify final warehouse record counts."""

    query = text(
        """
        SELECT
            (SELECT COUNT(*) FROM staging.stock_prices),
            (SELECT COUNT(*) FROM warehouse.fact_stock_prices),
            (SELECT COUNT(*) FROM staging.data_quality_errors)
        """
    )

    with engine.connect() as connection:
        staging_count, fact_count, quality_errors = (
            connection.execute(query).one()
        )

    print("\n=== DATABASE VERIFICATION ===")
    print(f"Staging records       : {staging_count:,}")
    print(f"Fact table records    : {fact_count:,}")
    print(f"Quality error records : {quality_errors:,}")

    if fact_count == 0:
        raise ValueError("Fact table is empty")

    print("✓ Database verification passed")


def main():

    print("======================================")
    print("       DATA WAREHOUSE ETL")
    print("======================================")

    print("\nStarting ETL pipeline...")

    # Extract
    df = extract_data(
        "data/raw/stocks.csv"
    )

    print(f"Records extracted: {len(df):,}")

    # Transform
    df = transform_data(df)

    print(f"Records transformed: {len(df):,}")

    # Validate
    errors = validate_data(df)

    if errors:
        print("\nData quality issues found:")

        for error in errors:
            print("-", error)

        print(
            "\nThese records will be handled "
            "by the PostgreSQL warehouse ETL."
        )

    else:
        print("\nData validation successful")

    # Database
    engine = get_database_engine()

    print("✓ PostgreSQL connection established")

    load_to_postgresql(
        df,
        engine
    )

    verify_warehouse(
        engine
    )

    print("\n======================================")
    print("       ETL PIPELINE COMPLETED")
    print("======================================")


if __name__ == "__main__":
    main()
