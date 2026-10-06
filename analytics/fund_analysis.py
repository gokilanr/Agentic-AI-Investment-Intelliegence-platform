import pandas as pd

from utils.logger import get_logger

from analytics.fund_profile import (
    get_fund_profile
)

from analytics.fund_intelligence import (
    analyze_fund_intelligence
)

logger = get_logger(__name__)


def build_fund_analysis(
    data: pd.DataFrame,
    ticker: str,
    fund_type: str = "ETF",
    risk_free_rate: float = 0.0,
) -> dict:
    """
    Build the complete mutual fund / ETF analysis.
    """

    logger.info(
        f"Building fund analysis for {ticker}."
    )

    profile = get_fund_profile(ticker)

    intelligence = analyze_fund_intelligence(
        data=data,
        fund_name=(
            profile.get("name")
            or ticker
        ),
        fund_type=fund_type,
        risk_free_rate=risk_free_rate,
    )

    result = {
        "profile": profile,
        "intelligence": intelligence,
    }

    logger.info(
        f"Fund analysis completed for {ticker}."
    )

    return result