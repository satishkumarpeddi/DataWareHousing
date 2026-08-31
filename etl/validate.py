"""
Data Quality Validation Module

Validates transformed stock market data before loading
it into the data warehouse.
"""

import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "volume",
    "ticker"
]


def validate_columns(df):
    """
    Check whether all required columns exist.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return True

def validate_nulls(df):
    """
    Find records containing NULL values
    in required columns.
    """

    errors = []

    for column in REQUIRED_COLUMNS:

        null_rows = df[df[column].isnull()]

        for index in null_rows.index:

            errors.append({
                "row_number": int(index),
                "ticker": df.loc[index, "ticker"],
                "date": df.loc[index, "date"],
                "error_type": "NULL_VALUE",
                "column_name": column,
                "error_message": (
                    f"NULL value found in {column}"
                )
            })

    return errors


def validate_positive_prices(df):
    """
    Check that stock prices are greater than zero.
    """

    errors = []

    price_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price"
    ]

    for column in price_columns:

        invalid_rows = df[
            df[column].notna() &
            (df[column] <= 0)
        ]

        for index in invalid_rows.index:

            errors.append({
                "row_number": int(index),
                "ticker": df.loc[index, "ticker"],
                "date": df.loc[index, "date"],
                "error_type": "INVALID_PRICE",
                "column_name": column,
                "error_message": (
                    f"{column} must be greater than zero"
                )
            })

    return errors


def validate_high_low(df):
    """
    Check that High price is greater than or equal
    to Low price.
    """

    errors = []

    invalid_rows = df[
        df["high_price"].notna() &
        df["low_price"].notna() &
        (df["high_price"] < df["low_price"])
    ]

    for index in invalid_rows.index:

        errors.append({
            "row_number": int(index),
            "ticker": df.loc[index, "ticker"],
            "date": df.loc[index, "date"],
            "error_type": "INVALID_PRICE_RANGE",
            "column_name": "high_price",
            "error_message": (
                "high_price is less than low_price"
            )
        })

    return errors


def validate_open_price(df):
    """
    Check that Open price falls between Low and High.
    """

    errors = []

    invalid_rows = df[
        df["open_price"].notna() &
        df["high_price"].notna() &
        df["low_price"].notna() &
        (
            (df["open_price"] < df["low_price"]) |
            (df["open_price"] > df["high_price"])
        )
    ]

    for index in invalid_rows.index:

        errors.append({
            "row_number": int(index),
            "ticker": df.loc[index, "ticker"],
            "date": df.loc[index, "date"],
            "error_type": "INVALID_OPEN_PRICE",
            "column_name": "open_price",
            "error_message": (
                "open_price is outside the "
                "low_price/high_price range"
            )
        })

    return errors


def validate_close_price(df):
    """
    Check that Close price falls between Low and High.
    """

    errors = []

    invalid_rows = df[
        df["close_price"].notna() &
        df["high_price"].notna() &
        df["low_price"].notna() &
        (
            (df["close_price"] < df["low_price"]) |
            (df["close_price"] > df["high_price"])
        )
    ]

    for index in invalid_rows.index:

        errors.append({
            "row_number": int(index),
            "ticker": df.loc[index, "ticker"],
            "date": df.loc[index, "date"],
            "error_type": "INVALID_CLOSE_PRICE",
            "column_name": "close_price",
            "error_message": (
                "close_price is outside the "
                "low_price/high_price range"
            )
        })

    return errors


def validate_volume(df):
    """
    Check that trading volume is not negative.
    """

    errors = []

    invalid_rows = df[
        df["volume"].notna() &
        (df["volume"] < 0)
    ]

    for index in invalid_rows.index:

        errors.append({
            "row_number": int(index),
            "ticker": df.loc[index, "ticker"],
            "date": df.loc[index, "date"],
            "error_type": "INVALID_VOLUME",
            "column_name": "volume",
            "error_message": (
                "Volume cannot be negative"
            )
        })

    return errors


def validate_ticker(df):
    """
    Check that ticker values are not NULL or empty.
    """

    errors = []

    invalid_rows = df[
        df["ticker"].isnull() |
        (
            df["ticker"]
            .astype(str)
            .str.strip()
            .eq("")
        )
    ]

    for index in invalid_rows.index:

        errors.append({
            "row_number": int(index),
            "ticker": df.loc[index, "ticker"],
            "date": df.loc[index, "date"],
            "error_type": "INVALID_TICKER",
            "column_name": "ticker",
            "error_message": (
                "Ticker cannot be NULL or empty"
            )
        })

    return errors


def validate_dates(df):
    """
    Check that dates are valid.
    """

    errors = []

    converted_dates = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    invalid_rows = df[
        converted_dates.isnull()
    ]

    for index in invalid_rows.index:

        errors.append({
            "row_number": int(index),
            "ticker": df.loc[index, "ticker"],
            "date": df.loc[index, "date"],
            "error_type": "INVALID_DATE",
            "column_name": "date",
            "error_message": (
                "Invalid date value"
            )
        })

    return errors


def validate_duplicates(df):
    """
    Check for duplicate date/ticker combinations.
    """

    errors = []

    duplicate_mask = df.duplicated(
        subset=["date", "ticker"],
        keep=False
    )

    duplicate_rows = df[
        duplicate_mask
    ]

    for index in duplicate_rows.index:

        errors.append({
            "row_number": int(index),
            "ticker": df.loc[index, "ticker"],
            "date": df.loc[index, "date"],
            "error_type": "DUPLICATE_RECORD",
            "column_name": "date,ticker",
            "error_message": (
                "Duplicate date/ticker combination"
            )
        })

    return errors


def validate_data(df):
    """
    Run all data-quality checks.

    Returns:
        list: Data-quality errors
    """

    if df is None:
        raise ValueError(
            "Cannot validate None dataframe"
        )

    if df.empty:
        raise ValueError(
            "Cannot validate empty dataframe"
        )

    validate_columns(df)

    errors = []

    errors.extend(validate_nulls(df))
    errors.extend(validate_positive_prices(df))
    errors.extend(validate_high_low(df))
    errors.extend(validate_open_price(df))
    errors.extend(validate_close_price(df))
    errors.extend(validate_volume(df))
    errors.extend(validate_ticker(df))
    errors.extend(validate_dates(df))
    errors.extend(validate_duplicates(df))

    return errors


def split_valid_invalid(df):
    """
    Split records into valid and invalid records.

    A record is considered invalid if it violates any
    data-quality rule.
    """

    errors = validate_data(df)

    if not errors:

        return df.copy(), pd.DataFrame()

    invalid_indices = {
        error["row_number"]
        for error in errors
    }

    invalid_df = df.loc[
        df.index.isin(invalid_indices)
    ].copy()

    valid_df = df.loc[
        ~df.index.isin(invalid_indices)
    ].copy()

    return valid_df, invalid_df


def create_error_dataframe(df):
    """
    Convert validation errors into a DataFrame.
    """

    errors = validate_data(df)

    if not errors:

        return pd.DataFrame(
            columns=[
                "row_number",
                "ticker",
                "date",
                "error_type",
                "column_name",
                "error_message"
            ]
        )

    return pd.DataFrame(errors)

if __name__ == "__main__":

    from etl.extract import extract_data
    from etl.transform import transform_data

    print("=== VALIDATION TEST ===")

    raw_data = extract_data()

    transformed_data = transform_data(
        raw_data
    )

    print(
        f"Records to validate: "
        f"{len(transformed_data)}"
    )

    errors = validate_data(
        transformed_data
    )

    print(
        f"Total quality errors: "
        f"{len(errors)}"
    )

    if errors:

        error_df = pd.DataFrame(errors)

        print("\n=== ERROR SUMMARY ===")

        print(
            error_df["error_type"]
            .value_counts()
        )

        print("\n=== SAMPLE ERRORS ===")

        print(
            error_df.head(20)
            .to_string(index=False)
        )

    else:

        print(
            "✓ No data-quality errors found"
        )