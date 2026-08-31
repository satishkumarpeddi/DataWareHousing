"""
Data Transformation Module

Transforms extracted stock market data into the
standardized format used by the data warehouse.
"""

import pandas as pd


# =========================================================
# TRANSFORMATION
# =========================================================

def transform_data(df):
    """
    Transform extracted stock data.

    Expected input columns:

        date
        open_price
        high_price
        low_price
        close_price
        volume
        ticker

    Returns:
        pandas.DataFrame
    """

    if df is None:
        raise ValueError("Input dataframe is None")

    if df.empty:
        raise ValueError("Input dataframe is empty")

    print("Starting data transformation...")

    # -----------------------------------------------------
    # Make a copy
    # -----------------------------------------------------

    df = df.copy()

    # -----------------------------------------------------
    # Standardize column names
    # -----------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # -----------------------------------------------------
    # Handle possible original dataset column names
    # -----------------------------------------------------

    rename_map = {
        "open": "open_price",
        "high": "high_price",
        "low": "low_price",
        "close": "close_price",
        "name": "ticker"
    }

    df.rename(
        columns=rename_map,
        inplace=True
    )

    # -----------------------------------------------------
    # Required columns
    # -----------------------------------------------------

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
            "Missing required columns after "
            f"transformation: {missing_columns}\n"
            f"Available columns: {list(df.columns)}"
        )

    # -----------------------------------------------------
    # Select required columns
    # -----------------------------------------------------

    df = df[
        required_columns
    ].copy()

    # -----------------------------------------------------
    # Convert date
    # -----------------------------------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # Convert price columns to numeric
    # -----------------------------------------------------

    price_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price"
    ]

    for column in price_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # -----------------------------------------------------
    # Convert volume to numeric
    # -----------------------------------------------------

    df["volume"] = pd.to_numeric(
        df["volume"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # Clean ticker
    # -----------------------------------------------------

    df["ticker"] = (
        df["ticker"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # -----------------------------------------------------
    # Remove completely empty rows
    # -----------------------------------------------------

    df.dropna(
        how="all",
        inplace=True
    )

    # -----------------------------------------------------
    # Sort data
    # -----------------------------------------------------

    df.sort_values(
        by=["ticker", "date"],
        inplace=True
    )

    # -----------------------------------------------------
    # Reset index
    # -----------------------------------------------------

    df.reset_index(
        drop=True,
        inplace=True
    )

    print(
        f"Records transformed: {len(df)}"
    )

    return df


# =========================================================
# MAIN TEST
# =========================================================

if __name__ == "__main__":

    from etl.extract import extract_data

    print("=== TRANSFORMATION TEST ===")

    raw_data = extract_data()

    transformed_data = transform_data(
        raw_data
    )

    print("\nTransformed columns:")

    print(
        transformed_data.columns.tolist()
    )

    print("\nFirst 5 records:")

    print(
        transformed_data.head()
    )

    print("\nData types:")

    print(
        transformed_data.dtypes
    )