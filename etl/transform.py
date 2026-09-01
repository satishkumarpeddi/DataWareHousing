"""
Data Transformation Module

Transforms extracted stock market data into the
standardized format used by the data warehouse.
"""

import pandas as pd



def transform_data(df):
    """
    Transform extracted stock market data.

    Expected input columns:

        date
        open_price
        high_price
        low_price
        close_price
        volume
        ticker

    Also supports the original dataset names:

        open
        high
        low
        close
        Name
    """

    if df is None:
        raise ValueError("Input dataframe is None")

    if df.empty:
        raise ValueError("Input dataframe is empty")

    print("Starting data transformation...")


    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )


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
            "Missing required columns after transformation: "
            f"{missing_columns}\n"
            f"Available columns: {list(df.columns)}"
        )


    df = df[required_columns].copy()


    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )


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


    df["volume"] = pd.to_numeric(
        df["volume"],
        errors="coerce"
    )


    df["ticker"] = (
        df["ticker"]
        .astype("string")
        .str.strip()
        .str.upper()
    )


    df.dropna(
        how="all",
        inplace=True
    )

    df.sort_values(
        by=["ticker", "date"],
        inplace=True
    )


    df.reset_index(
        drop=True,
        inplace=True
    )

    print(
        f"Records transformed: {len(df)}"
    )

    return df


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