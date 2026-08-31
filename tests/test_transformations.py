from etl.extract import extract_data
from etl.transform import transform_data


print("=== TRANSFORMATION TEST ===")

try:

    raw_df = extract_data()

    print(f"\nRaw records: {len(raw_df)}") 

    transformed_df = transform_data(raw_df)

    print(
        f"Transformed records: "
        f"{len(transformed_df)}"
    ) 

    print("\nTransformed columns:")

    print(
        transformed_df.columns.tolist()
    ) 

    print("\nData types:")

    print(
        transformed_df.dtypes
    ) 

    print("\nFirst 5 transformed records:")

    print(
        transformed_df
    ) 

    print("\nNULL values:")

    print(
        transformed_df.isnull().sum()
    ) 

    duplicate_count = transformed_df.duplicated(
        subset=["date", "ticker"]
    ).sum()

    print(
        f"\nDuplicate date/ticker records: "
        f"{duplicate_count}"
    )

    print("\nTransformation successful!")

except Exception as e:

    print("\nTransformation failed!")

    print(f"Error: {e}")