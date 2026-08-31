import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Load .env
load_dotenv()


# Read database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


print("=== ETL CONNECTION TEST ===")
print(f"Host: {DB_HOST}")
print(f"Port: {DB_PORT}")
print(f"Database: {DB_NAME}")
print(f"User: {DB_USER}")


try:

    database_url = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/"
        f"{DB_NAME}"
    )

    engine = create_engine(database_url)

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT version();")
        )

        version = result.fetchone()[0]

        print("\nPostgreSQL connection successful!")
        print(f"PostgreSQL version: {version}")


except Exception as e:

    print("\nPostgreSQL connection failed!")
    print(f"Error: {e}")