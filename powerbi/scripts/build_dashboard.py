"""
S&P 500 Analytics
Power BI Dashboard Validation Script

This script verifies that the PostgreSQL analytics
layer contains everything required by the Power BI dashboard.
"""

import json
import sys
from pathlib import Path

import psycopg2

import os

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "DataWarehouse"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")
}


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    BASE_DIR
    / "powerbi"
    / "model"
    / "model_definition.json"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def connect_database():

    print("Connecting to PostgreSQL...")

    try:

        connection = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )

        print("✓ PostgreSQL connection successful")

        return connection

    except Exception as error:

        print("✗ PostgreSQL connection failed")
        print(f"Error: {error}")

        sys.exit(1)


# ============================================================
# LOAD MODEL DEFINITION
# ============================================================

def load_model():

    print("\nLoading Power BI model definition...")

    try:

        with open(
            MODEL_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            model = json.load(file)

        print("✓ Model definition loaded")

        return model

    except Exception as error:

        print("✗ Could not load model definition")
        print(f"Error: {error}")

        sys.exit(1)


# ============================================================
# CHECK ANALYTICS VIEWS
# ============================================================

def check_views(connection, model):

    print("\nChecking analytics views...")

    cursor = connection.cursor()

    views = model["views"]

    failed = []

    for view_name, information in views.items():

        schema = information["schema"]
        table = information["table"]

        query = """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.views
                WHERE table_schema = %s
                AND table_name = %s
            );
        """

        cursor.execute(
            query,
            (schema, table)
        )

        exists = cursor.fetchone()[0]

        if exists:

            print(
                f"✓ {schema}.{table}"
            )

        else:

            print(
                f"✗ {schema}.{table} NOT FOUND"
            )

            failed.append(
                f"{schema}.{table}"
            )

    cursor.close()

    return failed


# ============================================================
# CHECK RECORD COUNTS
# ============================================================

def check_data(connection, model):

    print("\nChecking analytics data...")

    cursor = connection.cursor()

    for view_name, information in model["views"].items():

        schema = information["schema"]
        table = information["table"]

        query = f"""
            SELECT COUNT(*)
            FROM {schema}.{table};
        """

        cursor.execute(query)

        count = cursor.fetchone()[0]

        print(
            f"✓ {schema}.{table}: {count:,} records"
        )

    cursor.close()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("       S&P 500 POWER BI VALIDATION")
    print("=" * 60)

    model = load_model()

    connection = connect_database()

    failed_views = check_views(
        connection,
        model
    )

    if failed_views:

        print("\n✗ Missing analytics views:")

        for view in failed_views:
            print(f"  - {view}")

        connection.close()

        sys.exit(1)

    check_data(
        connection,
        model
    )

    connection.close()

    print("\n" + "=" * 60)
    print("✓ POWER BI DATA SOURCE VALIDATION PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()