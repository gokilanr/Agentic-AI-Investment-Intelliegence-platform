import yfinance as yf
import pandas as pd
from utils.logger import get_logger
from config.settings import RAW_DATA_DIR

logger = get_logger(__name__)

def fetch_stock_data(ticker:str, period:str = "5y") -> pd.DataFrame:
    """
    Fetch Historical stock market data.
    
    parameters
    ----------
    ticker : str
        stock ticker symbol
    period : str
        Historical period supported by yfinance.
        
    Returns
    -------
    pd.DataFrame
        Historical OHLCV data.
        
    """
    logger.info(f"Fetching market data for {ticker}")

    stock = yf.Ticker(ticker)

    data = stock.history(period=period)

    if data.empty:
        raise ValueError(f"No market data found for ticker: {ticker}")

    data = data.reset_index()

    logger.info(
        f"Sucessfully fetched {len(data)} rows for {ticker}"
    )

    return data


def save_stock_data(ticker: str, data:pd.DataFrame) -> None:
    """
    Save raw stock data as csv
    """

    file_name = f"{ticker.replace('.', '_')}_historical.csv"

    file_path = RAW_DATA_DIR/ file_name

    data.to_csv(file_path, index=False)

    logger.info(f"Data saved to: {file_path}")

if __name__ == "__main__":

    tickers = [
        "RELIANCE.NS",
        "AAPL"
    ]

    for ticker in tickers:

        try:
            stock_data = fetch_stock_data(ticker)

            logger.info(
                f"First 5 rows for {ticker}:\n{stock_data.head()}"
            )
            
            save_stock_data(ticker, stock_data)

        except Exception as error:

            logger.error(f"Failed to fetch data for {ticker}: {error}")