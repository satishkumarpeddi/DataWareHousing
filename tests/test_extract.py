from etl.extract import extract_data


print("=== EXTRACTION TEST ===")

try:

    df = extract_data()

    print("\nExtraction successful!")

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 records:")
    print(df.head())

except Exception as e:

    print("\nExtraction failed!")
    print(f"Error: {e}")