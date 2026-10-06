import yfinance as yf

from utils.logger import get_logger

logger = get_logger(__name__)


def get_fund_profile(ticker: str) -> dict:
    """
    Retrieve basic mutual fund / ETF information
    using Yahoo Finance metadata.
    """

    logger.info(
        f"Fetching fund profile for {ticker}."
    )

    fund = yf.Ticker(ticker)

    try:
        info = fund.info
    except Exception as error:
        logger.warning(
            f"Unable to retrieve profile for {ticker}: {error}"
        )
        info = {}

    return {
        "ticker": ticker,
        "name": (
            info.get("longName")
            or info.get("shortName")
        ),
        "category": info.get("category"),
        "fund_family": info.get("fundFamily"),
        "currency": info.get("currency"),
        "exchange": info.get("exchange"),
        "country": info.get("country"),
        "expense_ratio": info.get(
            "annualReportExpenseRatio"
        ),
        "total_assets": info.get("totalAssets"),
        "yield": info.get("yield"),
        "beta": info.get("beta3Year"),
        "morningstar_rating": info.get(
            "morningStarOverallRating"
        ),
    }