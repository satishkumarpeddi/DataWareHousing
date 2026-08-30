def transform_data(df):

    df.columns = df.columns.str.strip().str.lower()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.rename(columns={
        "open": "open_price",
        "high": "high_price",
        "low": "low_price",
        "close": "close_price"
    })

    df["ticker"] = df["name"].str.strip().str.upper()

    return df