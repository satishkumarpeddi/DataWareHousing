"""
Tests for the cleaned stock dataset.
"""

import pandas as pd


CLEAN_FILE = "data/processed/stocks_clean.csv"


def load_clean_data():

    df = pd.read_csv(
        CLEAN_FILE
    )

    return df


def test_no_null_values():

    df = load_clean_data()

    required_columns = [
        "date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
        "ticker"
    ]

    null_count = (
        df[required_columns]
        .isnull()
        .sum()
        .sum()
    )

    assert null_count == 0, (
        f"Found {null_count} NULL values"
    )

    print(
        "✓ No NULL values"
    )


def test_prices_positive():

    df = load_clean_data()

    price_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price"
    ]

    for column in price_columns:

        assert (
            df[column] > 0
        ).all(), (
            f"Invalid values in {column}"
        )

    print(
        "✓ All prices are positive"
    )


def test_high_low():

    df = load_clean_data()

    invalid = df[
        df["high_price"] < df["low_price"]
    ]

    assert invalid.empty, (
        f"Found {len(invalid)} High/Low errors"
    )

    print(
        "✓ High price >= Low price"
    )


def test_open_range():

    df = load_clean_data()

    invalid = df[
        (df["open_price"] < df["low_price"]) |
        (df["open_price"] > df["high_price"])
    ]

    assert invalid.empty, (
        f"Found {len(invalid)} invalid Open prices"
    )

    print(
        "✓ Open prices are valid"
    )


def test_close_range():

    df = load_clean_data()

    invalid = df[
        (df["close_price"] < df["low_price"]) |
        (df["close_price"] > df["high_price"])
    ]

    assert invalid.empty, (
        f"Found {len(invalid)} invalid Close prices"
    )

    print(
        "✓ Close prices are valid"
    )


def test_volume():

    df = load_clean_data()

    invalid = df[
        df["volume"] < 0
    ]

    assert invalid.empty, (
        f"Found {len(invalid)} negative volume records"
    )

    print(
        "✓ Volume values are valid"
    )


def test_duplicates():

    df = load_clean_data()

    duplicates = df.duplicated(
        subset=["date", "ticker"]
    )

    assert duplicates.sum() == 0, (
        f"Found {duplicates.sum()} duplicates"
    )

    print(
        "✓ No duplicate date/ticker records"
    )


def test_dates():

    df = load_clean_data()

    dates = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    assert dates.notna().all(), (
        "Invalid dates found"
    )

    print(
        "✓ Dates are valid"
    )


if __name__ == "__main__":

    print(
        "\n=== CLEAN DATA QUALITY TEST ===\n"
    )

    tests = [
        test_no_null_values,
        test_prices_positive,
        test_high_low,
        test_open_range,
        test_close_range,
        test_volume,
        test_duplicates,
        test_dates
    ]

    passed = 0
    failed = 0

    for test in tests:

        try:

            test()
            passed += 1

        except Exception as error:

            failed += 1

            print(
                f"✗ {test.__name__}"
            )

            print(
                f"  Error: {error}"
            )

    print("\n==============================")
    print(
        f"Tests Passed : {passed}"
    )
    print(
        f"Tests Failed : {failed}"
    )
    print("==============================")

    if failed:
        raise SystemExit(1)