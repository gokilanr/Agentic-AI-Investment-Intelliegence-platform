
from data.market_data import fetch_stock_data
from analytics.fund_intelligence import analyze_fund_intelligence
from analytics.fund_profile import get_fund_profile
from utils.logger import get_logger

logger = get_logger(__name__)


def run_fund_agent(
    ticker: str,
    period: str = "5y",
    fund_type: str = "ETF",
    risk_free_rate: float = 0.0,
) -> dict:
    """Fetch fund price data and generate fund intelligence."""

    if not ticker or not ticker.strip():
        raise ValueError("Ticker cannot be empty.")

    if not period or not period.strip():
        raise ValueError("Period cannot be empty.")

    if not fund_type or not fund_type.strip():
        raise ValueError("Fund type cannot be empty.")

    if risk_free_rate <= -1:
        raise ValueError("Risk-free rate must be greater than -1.")

    ticker = ticker.strip()
    fund_type = fund_type.strip()

    logger.info("Running fund agent for %s", ticker)

    data = fetch_stock_data(
        ticker=ticker,
        period=period,
    )

    profile = get_fund_profile(ticker)

    analysis = analyze_fund_intelligence(
        data=data,
        fund_name=profile.get("name") or ticker,
        fund_type=fund_type,
        risk_free_rate=risk_free_rate,
    )

    return {
        "agent": "fund_agent",
        "status": "success",
        "ticker": ticker,
        "period": period,
        "profile": profile,
        "analysis": analysis,
    }
