import pandas as pd
import numpy as np
from utils.logger import get_logger
from config.settings import RAW_DATA_DIR,PROCESSED_DATA_DIR

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
    Standardize basic market  data structure
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

    #Remove duplicate dates
    data = remove_duplicate_dates(data)

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
        (data["Low"] > data["Open"])
        | (data["Low"] > data["Close"])
        | (data["Low"] > data["Low"])
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

def calculate_daily_return(data:pd.DataFrame) -> pd.DataFrame:

    """
    Calculate simple daily return based on closing price.
    """

    logger.info("Calculating daily returns.")

    data["Daily_Return"] = data["Close"].pct_change()

    logger.info("Daily return calculation completed.")

    return data

def calculate_log_return(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate logarithmic daily return based on closing price.
    """

    logger.info("Calculating log returns.")

    data["Log_Return"] = np.log(
        data["Close"] / data["Close"].shift(1)
    )

    logger.info("Log return calculation completed.")

    return data

def calculate_moving_averages(data:pd.DataFrame) -> pd.DataFrame:
    """
    Calculate 20period simple moving average based on closing price,
    """

    logger.info("Calculating moving averages.")

    data["SMA_20"] = data["Close"].rolling(window=20).mean()
    data["SMA_50"] = data["Close"].rolling(window=50).mean()
    data["SMA_200"] =  data["Close"].rolling(window=200).mean()

    logger.info("Moving average calculation completed.")

    return data

def calculate_rolling_volatility(data:pd.DataFrame) -> pd.DataFrame:

    """
    Caculate 20 period rolling volatility based on daily  returns.
    """

    logger.info("Caculating rolling volatility.")

    data["Rolling_Volatility_20"] = (
        data["Daily_Return"]
        .rolling(window=20)
        .std()
    )

    data["Rolling_Volatility_50"] = (
            data["Daily_Return"]
            .rolling(window=50)
            .std()
        )

    data["Annualized_Volatility_20"] = (
        data["Rolling_Volatility_20"] * np.sqrt(252)
    )

    data["Annualized_Volatility_50"] = (
        data["Rolling_Volatility_50"] * np.sqrt(252)
    )

    logger.info("Rolling Volatitlity calculation commpleted.")

    return data

def calculate_momentum_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Caculate price momentum features.
    """

    logger.info("Caculating momentum features.")

    data["Momentum_20"] = (
        data["Close"] - data["Close"].shift(20)
    )

    data["Momentum_50"] = (
            data["Close"] - data["Close"].shift(50)
    )

    data["ROC_20"] = (
        data["Close"].pct_change(periods=20)
    )

    data["ROC_50"] = (
            data["Close"].pct_change(periods=50)
    )

    return data

def calculate_price_vs_moving_average(data: pd.DataFrame) -> pd.DataFrame:

    """
    Caculate the percentage difference between current pice and moving averages
    """

    logger.info("Caculating price vs moving average features.")

    data["Price_vs_SMA_20"] = (
        data["Close"] / data["SMA_20"]
    ) - 1

    data["Price_vs_SMA_50"] = (
        data["Close"] / data["SMA_50"]
    ) - 1

    data["Price_vs_SMA_200"] = (
        data["Close"] / data["SMA_200"]
    ) - 1

    logger.info("Price Vs moving avergae features calculation completed.")

    return data

def calculate_volume_features(data:pd.DataFrame) -> pd.DataFrame:
    """
    Caculate volume-based features.
    """

    logger.info("Caculating volume features.")

    data["Volume_Change"] = (
        data["Volume"].pct_change()
        .replace([np.inf, -np.inf], np.nan)
    )

    data["Volume_SMA_20"] = (
        data["Volume"].rolling(window=20).mean()
    )

    data["Volume_Ratio"] = (
        data["Volume"] / data["Volume_SMA_20"]
    )

    logger.info("Volume feature calculation completed.")

    return data

def remove_duplicate_dates(data:pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate trading dates.
    """
    duplicate_count = data["Date"].duplicated().sum()

    if duplicate_count == 0:
        logger.info("No duplicate dates found.")
        return data

    logger.warning(
        f"Found {duplicate_count} duplicate dates."
        "Keeping the last record for each date." 
    )

    data = data.drop_duplicates(
        subset=["Date"],
        keep = "last"
    ).reset_index(drop=True)

    logger.info(
        f"Removed {duplicate_count} duplicate date records."
    )

    return data

def validate_processed_features(data:pd.DataFrame) -> bool:
    """
    Validate that the final processed dataset
    contains the expected financial features.
    """

    required_features = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Daily_Return",
        "Log_Return",
        "SMA_20",
        "SMA_50",
        "SMA_200",
        "Rolling_Volatility_20",
        "Rolling_Volatility_50",
        "Annualized_Volatility_20",
        "Annualized_Volatility_50",
        "Momentum_20",
        "Momentum_50",
        "ROC_20",
        "ROC_50",
        "Price_vs_SMA_20",
        "Price_vs_SMA_50",
        "Price_vs_SMA_200",
        "Volume_Change",
        "Volume_SMA_20",
        "Volume_Ratio"
    ]

    missing_features = [
        feature
        for feature in required_features
        if feature not in data.columns
    ]

    if missing_features:
        logger.error(
            f"Missing processed features: {missing_features}"
        )
        return False

    logger.info("Processed feature validation passed.")

    return True

def validate_processed_data(data: pd.DataFrame) -> bool:
    """
    Validate the final processed dataset.
    """

    logger.info("Starting processed dataset validation.")

    if not validate_processed_features(data):
        return False

    numeric_columns = data.select_dtypes(
        include=np.number
    ).columns

    infinite_values = np.isinf(
        data[numeric_columns]
    ).sum().sum()

    if infinite_values > 0:
        logger.error(
            f"Found {infinite_values} infinite values."
        )

        return False

    logger.info(
        "Processed dataset validation passed."
    )

    return True

def save_processed_market_data( data:pd.DataFrame, ticker : str) -> None:
    """
    Save the Final feature- engineered market dataset.
    """

    logger.info(
        f"Saving processed market data for {ticker}."
    )

    file_name = f"{ticker.replace('.','_')}_processed.csv"
    file_path = PROCESSED_DATA_DIR / file_name

    data.to_csv(file_path, index=False)

    logger.info(
        f"Processed data saved to: {file_path}"
    )

def main():
    ticker = "RELIANCE.NS"

    file_path = (
        RAW_DATA_DIR / "RELIANCE_NS_historical.csv"
    )

    try:
        data = load_raw_market_data(file_path)

        data = standardize_market_data(data)

        if not validate_ohlc_relationship(data):
            raise ValueError(
                "Invalid OHLC relationship detected."
            )

        data = calculate_daily_return(data)

        data = calculate_log_return(data)

        data = calculate_moving_averages(data)

        data = calculate_rolling_volatility(data)

        data = calculate_momentum_features(data)

        data = calculate_price_vs_moving_average(data)

        data = calculate_volume_features(data)

        if not validate_processed_data(data):
            raise ValueError(
                "Processed dataset validation failed."
            )

        save_processed_market_data(
            data,
            ticker
        )

        logger.info(
            "Market data processing pipeline completed successfully."
        )

    except Exception as error:
        logger.error(
            f"Market data processing failed: {error}"
        )
        raise


if __name__ == "__main__":
    main()