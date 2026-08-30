import os


# ============================================
# PROJECT CONFIGURATION
# ============================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# ============================================
# DATA PATHS
# ============================================

RAW_DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
    "raw"
)

RAW_FILE = os.path.join(
    RAW_DATA_DIR,
    "stocks.csv"
)


# ============================================
# LOGGING
# ============================================

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)


# ============================================
# DATABASE CONFIGURATION
# ============================================

DB_HOST = os.getenv(
    "DB_HOST",
    "localhost"
)

DB_PORT = os.getenv(
    "DB_PORT",
    "5432"
)

DB_NAME = os.getenv(
    "DB_NAME",
    "DataWarehouse"
)

DB_USER = os.getenv(
    "DB_USER",
    "postgres"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
    ""
)


# ============================================
# SCHEMAS
# ============================================

STAGING_SCHEMA = "staging"

WAREHOUSE_SCHEMA = "warehouse"

ANALYTICS_SCHEMA = "analytics"


# ============================================
# TABLES
# ============================================

STAGING_TABLE = "stock_prices"

FACT_TABLE = "fact_stock_prices"

DATE_DIMENSION = "dim_date"

COMPANY_DIMENSION = "dim_company"

DATA_QUALITY_TABLE = "data_quality_errors"

LOAD_METADATA_TABLE = "load_metadata"