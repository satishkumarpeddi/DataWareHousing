import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform raw stock data into the structure required
    by the staging.stock_prices table.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw stock data.

    Returns
    -------
    pandas.DataFrame
        Transformed stock data.
    """

    print("Starting data transformation...")

    # --------------------------------------------------------
    # Make a copy
    # --------------------------------------------------------

    df = df.copy()

    # --------------------------------------------------------
    # Normalize column names
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # --------------------------------------------------------
    # Validate required source columns
    # --------------------------------------------------------

    required_columns = {
        "date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
        "ticker"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # --------------------------------------------------------
    # Rename columns
    # --------------------------------------------------------

    column_mapping = {
        "open_price": "open_price",
        "high_price": "high_price",
        "low_price": "low_price",
        "close_price": "close_price",
        "ticker": "ticker"
    }

    df = df.rename(columns=column_mapping)

    # --------------------------------------------------------
    # Convert date
    # --------------------------------------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    ).dt.date

    # --------------------------------------------------------
    # Convert price columns
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Convert volume
    # --------------------------------------------------------

    df["volume"] = pd.to_numeric(
        df["volume"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Normalize ticker
    # --------------------------------------------------------

    df["ticker"] = (
        df["ticker"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # --------------------------------------------------------
    # Keep only staging columns
    # --------------------------------------------------------

    df = df[
        [
            "date",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "volume",
            "ticker"
        ]
    ]

    # --------------------------------------------------------
    # Sort data
    # --------------------------------------------------------

    df = df.sort_values(
        by=["ticker", "date"]
    ).reset_index(drop=True)

    print(f"Records transformed: {len(df)}")

    return df