from utils.logger import get_logger

from analytics.company_profile import (
    get_company_profile
)

from analytics.stock_intelligence import (
    analyze_stock_intelligence
)


logger = get_logger(__name__)


def build_company_intelligence(
    data,
    ticker: str,
    risk_free_rate: float = 0.0
) -> dict:
    """
    Build the complete company intelligence object.
    """

    logger.info(
        f"Building company intelligence for {ticker}."
    )

    profile = get_company_profile(
        ticker
    )

    stock_analysis = analyze_stock_intelligence(
        data,
        ticker,
        risk_free_rate
    )

    result = {
        "company": profile,
        "stock_analysis": stock_analysis,
    }

    logger.info(
        f"Company intelligence completed for {ticker}."
    )

    return result