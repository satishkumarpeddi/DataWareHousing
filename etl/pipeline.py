from extract import extract_data
from transform import transform_data
from validate import validate_data


def main():

    print("Starting ETL pipeline...")

    # Extract
    df = extract_data(
        "data/raw/stocks.csv"
    )

    # Transform
    df = transform_data(df)

    # Validate
    errors = validate_data(df)

    if errors:
        print("Data quality issues found:")

        for error in errors:
            print("-", error)

        return

    print("Data validation successful")

    # Load
    # load_data(df)

    print("ETL pipeline completed")


if __name__ == "__main__":
    main()