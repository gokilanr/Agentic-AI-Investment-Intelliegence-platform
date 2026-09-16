import pandas as pd

from utils.logger import get_logger
from config.settings import RAW_DATA_DIR

logger = get_logger(__name__)

def load_raw_market_data(file_path) -> pd.DataFrame:
    """
    Load raw market data from a CSV file.
    """

    logger.info(f"Loading raw market data from: {file_path}")

    data = pd.read_csv(file_path)

    logger.info(
        f"loaded {len(data)} rows and {len(data.columns)} columns"
    )

    return data

def standardize_market_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize basic market  data sstructure
    """
    logger.info("Starting market data standardization.")

    #standardize column names
    data.columns = [
        column.strip()
        for column in data.columns
    ]

    #convert date column to datetime
    data["Date"] = pd.to_datetime(data["Date"])

    #sort data chronologically
    data = data.sort_values("Date").reset_index(drop=True)

    logger.info("Market data standardization completed.")

    logger.info(
    f"Date data type: {data['Date'].dtype}"
)

    return data

def validate_ohlc_relationship(data:pd.DataFrame) -> bool:
    """
    Validate logical relationships between OHLC prices.
    """
    logger.info("Starting OHLC relationship validation.")

    invalid_high = (
        (data["High"] < data["Open"])
        | (data["High"] < data["Close"])
        | (data["High"] < data["Low"])
    )

    invalid_low = (
        (data["Low"] < data["Open"])
        | (data["Low"] < data["Close"])
        | (data["Low"] < data["Low"])
    )

    invalid_rows = invalid_high | invalid_low

    invalid_count = invalid_rows.sum()

    if invalid_count > 0:
        logger.error(
            f"Found {invalid_count} rows with invalid OHLC relationships."
        )

        return False
    logger.info("OHLC relationship validation passed.")

    return True
#remiaining is still is there codes

if __name__ == "__main__":

    file_path = RAW_DATA_DIR / "RELIANCE_NS_historical.csv"

    data = load_raw_market_data(file_path)

    data = standardize_market_data(data)

    logger.info(
        f"Date range: {data['Date'].min()} to {data['Date'].max()}"
    )

    logger.info(
        f"First 5 rows:\n{data.head()}"
    )