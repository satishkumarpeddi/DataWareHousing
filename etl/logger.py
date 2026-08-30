import logging
import os
from datetime import datetime


def setup_logger():

    os.makedirs("logs", exist_ok=True)

    log_file = (
        f"logs/etl_{datetime.now().strftime('%Y%m%d')}.log"
    )

    logger = logging.getLogger("DataWarehouseETL")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger