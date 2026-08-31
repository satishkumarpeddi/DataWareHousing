import pandas as pd

from etl.config import RAW_FILE


def extract_data(file_path=RAW_FILE):
    """
    Extract raw stock data from the CSV file.

    The extraction layer only reads the source data.
    Transformation and cleaning are handled separately.
    """

    df = pd.read_csv(file_path)
    print(__doc__)
    print(f"Records extracted: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    return df