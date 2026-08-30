def validate_data(df):

    required_columns = [
        "date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
        "ticker"
    ]

    errors = []

    for column in required_columns:
        null_count = df[column].isna().sum()

        if null_count > 0:
            errors.append(
                f"{column}: {null_count} NULL values"
            )

    invalid_prices = df[
        (df["open_price"] <= 0) |
        (df["high_price"] <= 0) |
        (df["low_price"] <= 0) |
        (df["close_price"] <= 0)
    ]

    if len(invalid_prices) > 0:
        errors.append(
            f"Invalid prices: {len(invalid_prices)}"
        )

    invalid_volume = df[df["volume"] < 0]

    if len(invalid_volume) > 0:
        errors.append(
            f"Negative volume: {len(invalid_volume)}"
        )

    duplicate_count = df.duplicated(
        subset=["date", "ticker"]
    ).sum()

    if duplicate_count > 0:
        errors.append(
            f"Duplicate records: {duplicate_count}"
        )

    return errors