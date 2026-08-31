"""
Data Quality Tests

Tests the quality and consistency of stock market data
after extraction and transformation.

Dataset:
- date
- open_price
- high_price
- low_price
- close_price
- volume
- ticker
"""

import pandas as pd

print("TEST_QUALITY.PY STARTED")



def load_test_data():
    """
    Extract and transform data for quality testing.
    """

    from etl.extract import extract_data
    from etl.transform import transform_data

    raw_data = extract_data()

    if raw_data is None:
        raise ValueError("Extraction returned None")

    transformed_data = transform_data(raw_data)

    if transformed_data is None:
        raise ValueError("Transformation returned None")

    return transformed_data


def test_data_not_empty():

    df = load_test_data()

    assert df is not None, "DataFrame is None"
    assert not df.empty, "DataFrame is empty"

    print("✓ Test passed: Data is not empty")


def test_required_columns():

    df = load_test_data()

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

    assert not missing_columns, (
        f"Missing required columns: {missing_columns}"
    )

    print("✓ Test passed: Required columns exist")


def test_no_null_values():

    df = load_test_data()

    required_columns = [
        "date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
        "ticker"
    ]

    null_counts = df[required_columns].isnull().sum()

    print("\nNULL VALUES:")
    print(null_counts)

    invalid_columns = null_counts[null_counts > 0]

    assert invalid_columns.empty, (
        "NULL values found:\n"
        f"{invalid_columns}"
    )

    print("✓ Test passed: No NULL values")


def test_positive_prices():

    df = load_test_data()

    price_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price"
    ]

    problems = {}

    for column in price_columns:

        invalid_rows = df[
            df[column].notna() &
            (df[column] <= 0)
        ]

        if not invalid_rows.empty:
            problems[column] = len(invalid_rows)

    assert not problems, (
        f"Non-positive price values found: {problems}"
    )

    print("✓ Test passed: All prices are positive")



def test_high_greater_than_low():

    df = load_test_data()

    invalid_rows = df[
        df["high_price"].notna() &
        df["low_price"].notna() &
        (df["high_price"] < df["low_price"])
    ]

    if not invalid_rows.empty:

        print("\n=== HIGH < LOW RECORDS ===")

        print(
            invalid_rows[
                [
                    "date",
                    "ticker",
                    "open_price",
                    "high_price",
                    "low_price",
                    "close_price"
                ]
            ].to_string(index=False)
        )

    assert invalid_rows.empty, (
        f"Found {len(invalid_rows)} records "
        "where high_price < low_price"
    )

    print("✓ Test passed: High price >= Low price")


def test_price_range():

    df = load_test_data()

    # Invalid Open prices
    invalid_open = df[
        df["open_price"].notna() &
        df["high_price"].notna() &
        df["low_price"].notna() &
        (
            (df["open_price"] < df["low_price"]) |
            (df["open_price"] > df["high_price"])
        )
    ]

    # Invalid Close prices
    invalid_close = df[
        df["close_price"].notna() &
        df["high_price"].notna() &
        df["low_price"].notna() &
        (
            (df["close_price"] < df["low_price"]) |
            (df["close_price"] > df["high_price"])
        )
    ]

    if not invalid_open.empty:

        print("\n=== INVALID OPEN PRICE RECORDS ===")

        print(
            invalid_open[
                [
                    "date",
                    "ticker",
                    "open_price",
                    "high_price",
                    "low_price",
                    "close_price"
                ]
            ].to_string(index=False)
        )

    if not invalid_close.empty:

        print("\n=== INVALID CLOSE PRICE RECORDS ===")

        print(
            invalid_close[
                [
                    "date",
                    "ticker",
                    "open_price",
                    "high_price",
                    "low_price",
                    "close_price"
                ]
            ].to_string(index=False)
        )

    assert invalid_open.empty, (
        f"Invalid open prices found: {len(invalid_open)}"
    )

    assert invalid_close.empty, (
        f"Invalid close prices found: {len(invalid_close)}"
    )

    print(
        "✓ Test passed: Open and Close prices "
        "are within High/Low range"
    )


def test_volume_not_negative():

    df = load_test_data()

    invalid_volume = df[
        df["volume"].notna() &
        (df["volume"] < 0)
    ]

    if not invalid_volume.empty:

        print("\n=== NEGATIVE VOLUME RECORDS ===")

        print(
            invalid_volume[
                [
                    "date",
                    "ticker",
                    "volume"
                ]
            ].to_string(index=False)
        )

    assert invalid_volume.empty, (
        f"Negative volume values found: "
        f"{len(invalid_volume)}"
    )

    print("✓ Test passed: Volume is not negative")


def test_ticker_not_empty():

    df = load_test_data()

    invalid_tickers = df[
        df["ticker"].isnull() |
        (
            df["ticker"]
            .astype(str)
            .str.strip()
            .eq("")
        )
    ]

    if not invalid_tickers.empty:

        print("\n=== INVALID TICKER RECORDS ===")

        print(
            invalid_tickers[
                ["date", "ticker"]
            ].to_string(index=False)
        )

    assert invalid_tickers.empty, (
        f"Empty or NULL ticker values found: "
        f"{len(invalid_tickers)}"
    )

    print("✓ Test passed: Ticker values are valid")


def test_valid_dates():

    df = load_test_data()

    converted_dates = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    invalid_dates = df[
        converted_dates.isnull()
    ]

    if not invalid_dates.empty:

        print("\n=== INVALID DATE RECORDS ===")

        print(
            invalid_dates[
                ["date", "ticker"]
            ].to_string(index=False)
        )

    assert invalid_dates.empty, (
        f"Invalid dates found: {len(invalid_dates)}"
    )

    print("✓ Test passed: Dates are valid")



def test_no_duplicates():

    df = load_test_data()

    duplicate_mask = df.duplicated(
        subset=["date", "ticker"],
        keep=False
    )

    duplicate_rows = df[
        duplicate_mask
    ]

    duplicate_count = len(duplicate_rows)

    print(
        f"\nDuplicate date/ticker records: "
        f"{duplicate_count}"
    )

    if not duplicate_rows.empty:

        print("\n=== DUPLICATE RECORDS ===")

        print(
            duplicate_rows[
                [
                    "date",
                    "ticker",
                    "open_price",
                    "high_price",
                    "low_price",
                    "close_price",
                    "volume"
                ]
            ].to_string(index=False)
        )

    assert duplicate_rows.empty, (
        f"Found {duplicate_count} duplicate records"
    )

    print("✓ Test passed: No duplicate records")


def inspect_null_values():

    df = load_test_data()

    price_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price"
    ]

    null_rows = df[
        df[price_columns]
        .isnull()
        .any(axis=1)
    ]

    print("\n=== NULL PRICE RECORDS ===")

    if null_rows.empty:

        print("No NULL price records found.")

    else:

        print(
            null_rows[
                [
                    "date",
                    "ticker",
                    "open_price",
                    "high_price",
                    "low_price",
                    "close_price",
                    "volume"
                ]
            ].to_string(index=False)
        )

        print(
            f"\nTotal NULL price records: "
            f"{len(null_rows)}"
        )

def inspect_invalid_high_low():

    df = load_test_data()

    invalid_rows = df[
        df["high_price"].notna() &
        df["low_price"].notna() &
        (df["high_price"] < df["low_price"])
    ]

    print("\n=== HIGH < LOW RECORDS ===")

    if invalid_rows.empty:

        print("No High < Low records found.")

    else:

        print(
            invalid_rows[
                [
                    "date",
                    "ticker",
                    "open_price",
                    "high_price",
                    "low_price",
                    "close_price",
                    "volume"
                ]
            ].to_string(index=False)
        )

        print(
            f"\nTotal invalid records: "
            f"{len(invalid_rows)}"
        )



def inspect_invalid_price_range():

    df = load_test_data()

    invalid_open = df[
        df["open_price"].notna() &
        df["high_price"].notna() &
        df["low_price"].notna() &
        (
            (df["open_price"] < df["low_price"]) |
            (df["open_price"] > df["high_price"])
        )
    ]

    invalid_close = df[
        df["close_price"].notna() &
        df["high_price"].notna() &
        df["low_price"].notna() &
        (
            (df["close_price"] < df["low_price"]) |
            (df["close_price"] > df["high_price"])
        )
    ]

    print("\n=== INVALID PRICE RANGE RECORDS ===")

    print(
        f"\nInvalid Open records: "
        f"{len(invalid_open)}"
    )

    if not invalid_open.empty:

        print(
            invalid_open[
                [
                    "date",
                    "ticker",
                    "open_price",
                    "high_price",
                    "low_price",
                    "close_price"
                ]
            ].to_string(index=False)
        )

    print(
        f"\nInvalid Close records: "
        f"{len(invalid_close)}"
    )

    if not invalid_close.empty:

        print(
            invalid_close[
                [
                    "date",
                    "ticker",
                    "open_price",
                    "high_price",
                    "low_price",
                    "close_price"
                ]
            ].to_string(index=False)
        )

if __name__ == "__main__":

    print("\n=== DATA QUALITY TEST ===\n")

    tests = [
        test_data_not_empty,
        test_required_columns,
        test_no_null_values,
        test_positive_prices,
        test_high_greater_than_low,
        test_price_range,
        test_volume_not_negative,
        test_ticker_not_empty,
        test_valid_dates,
        test_no_duplicates
    ]

    passed = 0
    failed = 0

    failed_tests = []

    for test in tests:

        try:

            test()
            passed += 1

        except Exception as error:

            failed += 1
            failed_tests.append(test.__name__)

            print(
                f"✗ Test failed: {test.__name__}"
            )

            print(
                f"  Error: {error}"
            )

    if failed > 0:

        print("\n")
        print("=" * 60)
        print("DATA QUALITY DIAGNOSTICS")
        print("=" * 60)

        if "test_no_null_values" in failed_tests:
            inspect_null_values()

        if "test_high_greater_than_low" in failed_tests:
            inspect_invalid_high_low()

        if "test_price_range" in failed_tests:
            inspect_invalid_price_range()

    print("\n")
    print("=" * 60)
    print("DATA QUALITY TEST SUMMARY")
    print("=" * 60)

    print(f"Total Tests  : {len(tests)}")
    print(f"Tests Passed : {passed}")
    print(f"Tests Failed : {failed}")

    if failed_tests:

        print("\nFailed Tests:")

        for test_name in failed_tests:
            print(f"  - {test_name}")

    else:

        print("\n🎉 All data quality tests passed!")

    print("=" * 60)

    if failed > 0:
        raise SystemExit(1)