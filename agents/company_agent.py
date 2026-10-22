
from data.market_data import fetch_stock_data
from agents.stock_agent import prepare_stock_data
from analytics.company_intelligence import build_company_intelligence
from utils.logger import get_logger

logger = get_logger(__name__)


def run_company_agent(
    ticker: str,
    period: str = "5y",
    risk_free_rate: float = 0.0,
) -> dict:
    """Fetch market data and build company intelligence."""

    if not ticker or not ticker.strip():
        raise ValueError("Ticker cannot be empty.")

    if not period or not period.strip():
        raise ValueError("Period cannot be empty.")

    ticker = ticker.strip()

    logger.info("Running company agent for %s", ticker)

    raw_data = fetch_stock_data(
        ticker=ticker,
        period=period,
    )

    processed_data = prepare_stock_data(raw_data)

    report = build_company_intelligence(
        data=processed_data,
        ticker=ticker,
        risk_free_rate=risk_free_rate,
    )

    return {
        "agent": "company_agent",
        "status": "success",
        "ticker": ticker,
        "period": period,
        "analysis": report,
    }
