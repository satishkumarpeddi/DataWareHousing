"""
Source Data Cleaning Module

Creates a clean dataset from the transformed stock data.
"""

import pandas as pd
from pathlib import Path

from etl.extract import extract_data
from etl.transform import transform_data


def clean_data(df):
    """
    Remove invalid and duplicate stock records.
    """

    print("\n=== SOURCE DATA CLEANING ===")

    original_count = len(df)

    # -----------------------------------------------------
    # 1. Remove rows with NULL required values
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

    before = len(df)

    df = df.dropna(
        subset=required_columns
    ).copy()

    print(
        f"NULL records removed: "
        f"{before - len(df)}"
    )

    # -----------------------------------------------------
    # 2. Remove non-positive prices
    # -----------------------------------------------------

    before = len(df)

    price_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price"
    ]

    for column in price_columns:
        df = df[df[column] > 0]

    print(
        f"Invalid price records removed: "
        f"{before - len(df)}"
    )

    # -----------------------------------------------------
    # 3. Remove High < Low
    # -----------------------------------------------------

    before = len(df)

    df = df[
        df["high_price"] >= df["low_price"]
    ].copy()

    print(
        f"High < Low records removed: "
        f"{before - len(df)}"
    )

    # -----------------------------------------------------
    # 4. Remove invalid Open prices
    # -----------------------------------------------------

    before = len(df)

    df = df[
        (df["open_price"] >= df["low_price"]) &
        (df["open_price"] <= df["high_price"])
    ].copy()

    print(
        f"Invalid Open price records removed: "
        f"{before - len(df)}"
    )

    # -----------------------------------------------------
    # 5. Remove invalid Close prices
    # -----------------------------------------------------

    before = len(df)

    df = df[
        (df["close_price"] >= df["low_price"]) &
        (df["close_price"] <= df["high_price"])
    ].copy()

    print(
        f"Invalid Close price records removed: "
        f"{before - len(df)}"
    )

    # -----------------------------------------------------
    # 6. Remove negative volume
    # -----------------------------------------------------

    before = len(df)

    df = df[
        df["volume"] >= 0
    ].copy()

    print(
        f"Negative volume records removed: "
        f"{before - len(df)}"
    )

    # -----------------------------------------------------
    # 7. Remove invalid ticker
    # -----------------------------------------------------

    before = len(df)

    df = df[
        df["ticker"].notna() &
        (
            df["ticker"]
            .astype(str)
            .str.strip()
            .ne("")
        )
    ].copy()

    print(
        f"Invalid ticker records removed: "
        f"{before - len(df)}"
    )

    # -----------------------------------------------------
    # 8. Remove invalid dates
    # -----------------------------------------------------

    before = len(df)

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["date"]
    )

    print(
        f"Invalid date records removed: "
        f"{before - len(df)}"
    )

    # -----------------------------------------------------
    # 9. Remove duplicates
    # -----------------------------------------------------

    before = len(df)

    df = df.drop_duplicates(
        subset=["date", "ticker"],
        keep="first"
    )

    print(
        f"Duplicate records removed: "
        f"{before - len(df)}"
    )

    # -----------------------------------------------------
    # 10. Sort data
    # -----------------------------------------------------

    df = df.sort_values(
        by=["ticker", "date"]
    )

    # -----------------------------------------------------
    # 11. Reset index
    # -----------------------------------------------------

    df = df.reset_index(
        drop=True
    )

    cleaned_count = len(df)

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print("\n=== CLEANING SUMMARY ===")

    print(
        f"Original records : {original_count:,}"
    )

    print(
        f"Clean records    : {cleaned_count:,}"
    )

    print(
        f"Removed records  : "
        f"{original_count - cleaned_count:,}"
    )

    print(
        f"Remaining records: {len(df):,}"
    )

    return df


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=== CLEAN STOCK DATA ===")

    # Extract
    raw_data = extract_data()

    # Transform
    transformed_data = transform_data(
        raw_data
    )

    # Clean
    clean_data_result = clean_data(
        transformed_data
    )

    # -----------------------------------------------------
    # Create processed directory
    # -----------------------------------------------------

    output_directory = Path(
        "data/processed"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------------------
    # Save clean data
    # -----------------------------------------------------

    output_file = (
        output_directory /
        "stocks_clean.csv"
    )

    clean_data_result.to_csv(
        output_file,
        index=False
    )

    print(
        f"\n✓ Clean dataset created:"
        f"\n{output_file}"
    )