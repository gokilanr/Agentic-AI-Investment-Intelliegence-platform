import pandas as pd

from config.settings import RAW_DATA_DIR
from data.data_validator import validate_market_data
from utils.logger import get_logger

logger = get_logger(__name__)

def validate_csv_file(file_path):
    """
    Load csv file and validate its market data.
    """

    logger.info(f"lodaing file: {file_path}")

    data =pd.read_csv(file_path)

    logger.info(
        f"loaded {len(data)} rows and {len(data.columns)} columns."
    )

    is_valid = validate_market_data(data)

    if is_valid:
        logger.info(
            f"Validation passed for {file_path.name}"
        )

    else:
        logger.info(
            f"validation failed for {file_path.name}"

        )

    return is_valid

def main():
    """
    Validate all CSv files inisde the raw data directory.
    """

    csv_files = list(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        logger.warning(
            "No CSV files found in raw dataa directory."
        )

        return

    logger.info(
        f"Found {len(csv_files)} CSV file(s) to validate."
    )

    all_valid = True

    for file_path in csv_files:
        try:
            is_valid = validate_csv_file(file_path)

            if not is_valid:
                all_valid = False

        except Exception as error:
            logger.error(
                f"Error validating {file_path.name}: {error}"
            )

            all_valid = False


    if all_valid:
        logger.info(
            "All raw market data files passed validation."

        )

    else:
        logger.error(
            "one or more raw market data files failed validation."


        )


if __name__ == "__main__":
    main()