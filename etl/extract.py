import pandas as pd

from etl.config import RAW_FILE


def extract_data(file_path=RAW_FILE):
    """
    Extract stock data from the raw CSV file.
    """

    df = pd.read_csv(file_path)

    print(f"Records extracted: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    return df