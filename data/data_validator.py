import pandas as pd

from utils.logger import get_logger

logger = get_logger(__name__)

REQUIRED_COLUMNS = [
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]

def validate_columns(data:pd.DataFrame) -> bool:
    """
    Validate that all required columns exist.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        logger.error(
            f"Missing required columns: {missing_columns}"
        )

        return False

    logger.info("Required Columns Validation passed.")

    return True

def validate_missing_values(data:pd.DataFrame) -> bool:

    """
    Check for missing values in required columns
    """

    missing_values = data[REQUIRED_COLUMNS].isnull().sum()

    total_missing = missing_values.sum()

    if total_missing > 0:

        logger.error(
            f"Missing values detected:\n{missing_values}"
        )

        return False

    logger.info("Missing-Value validation passed.")

    return True


def validate_duplicate_dates(data: pd.DataFrame) -> bool:
    """
    Check for duplicate dates
    """

    duplicate_count = data["Date"].duplicated().sum()

    if duplicate_count > 0:

        logger.error(
            f"Found {duplicate_count} duplicate dates."
        )

        return False

    logger.info("Duplicate-date validation passed.")

    return True

def validate_prices(data: pd.DataFrame) -> bool:
    """
    Validate that price values are positive
    """

    price_columns = [
        "Open",
        "High",
        "Low",
        "Close"
    ]

    invalid_prices = (data[price_columns]<=0).sum().sum()

    if invalid_prices > 0:

        logger.error(
            f"Found {invalid_prices} invalid price values."
        )

        return False


    logger.info("Price validation passed.")

    return True


def validate_volume(data: pd.DataFrame) -> bool:

    """
    Validate that volume values are non-negative.
    """

    invalid_volume = (data["Volume"]<0).sum()

    if invalid_volume > 0:

        logger.error(
            f"Found {invalid_volume} invalid volume values."

        )

        return  False

    logger.info("Volume validaton passed.")

    return True


def validate_market_data(data: pd.DataFrame) -> bool:

    """
    Run all market-data validation checks.
    """

    logger.info("Starting market data validation.")
    #1 Validate required columns first
    if not validate_columns(data):
        logger.error("Market data Validation Failed.")
        return False
    
    #2 reun remaining validations
    validations = [
        
        validate_missing_values(data),
        validate_duplicate_dates(data),
        validate_prices(data),
        validate_volume(data)
    ]

    is_valid = all(validations)

    if is_valid:

        logger.info(
            "Market data validation Passed."

        )

    else:

        logger.error(
            "Market data validation Failed."
        )

    return is_valid
