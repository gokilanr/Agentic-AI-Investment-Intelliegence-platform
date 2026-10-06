import yfinance as yf

from utils.logger import get_logger

logger = get_logger(__name__)


def get_company_profile(
    ticker: str
) -> dict:
    """
    Retrieve basic company profile information.
    """

    logger.info(
        f"Fetching company profile for {ticker}."
    )

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "ticker": ticker,
        "company_name": info.get(
            "longName"
        ),
        "sector": info.get(
            "sector"
        ),
        "industry": info.get(
            "industry"
        ),
        "country": info.get(
            "country"
        ),
        "exchange": info.get(
            "exchange"
        ),
        "website": info.get(
            "website"
        ),
        "market_cap": info.get(
            "marketCap"
        ),
    }