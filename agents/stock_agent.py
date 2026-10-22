
import pandas as pd

from data.market_data import fetch_stock_data
from data.data_processor import (
    standardize_market_data,
    validate_ohlc_relationship,
    calculate_daily_return,
    calculate_log_return,
    calculate_moving_averages,
    calculate_rolling_volatility,
    calculate_momentum_features,
    calculate_price_vs_moving_average,
    calculate_volume_features,
    validate_processed_data,
    validate_feature_quality,
)
from analytics.stock_intelligence import analyze_stock_intelligence
from utils.logger import get_logger

logger = get_logger(__name__)


def prepare_stock_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate and engineer features for stock analysis."""

    if data.empty:
        raise ValueError("Stock market data cannot be empty.")

    data = standardize_market_data(data)

    if not validate_ohlc_relationship(data):
        raise ValueError("Invalid OHLC relationships in stock data.")

    data = calculate_daily_return(data)
    data = calculate_log_return(data)
    data = calculate_moving_averages(data)
    data = calculate_rolling_volatility(data)
    data = calculate_momentum_features(data)
    data = calculate_price_vs_moving_average(data)
    data = calculate_volume_features(data)

    if not validate_processed_data(data):
        raise ValueError("Processed stock data validation failed.")

    if not validate_feature_quality(data):
        raise ValueError("Stock feature quality validation failed.")

    return data


def run_stock_agent(
    ticker: str,
    period: str = "5y",
    risk_free_rate: float = 0.0,
) -> dict:
    """
    Fetch stock data, prepare features, and run stock intelligence.
    """

    if not ticker or not ticker.strip():
        raise ValueError("Ticker cannot be empty.")

    if not period or not period.strip():
        raise ValueError("Period cannot be empty.")

    logger.info("Running stock agent for %s", ticker)

    raw_data = fetch_stock_data(
        ticker=ticker.strip(),
        period=period,
    )

    processed_data = prepare_stock_data(raw_data)

    report = analyze_stock_intelligence(
        data=processed_data,
        ticker=ticker.strip(),
        risk_free_rate=risk_free_rate,
    )

    return {
        "agent": "stock_agent",
        "status": "success",
        "ticker": ticker.strip(),
        "period": period,
        "analysis": report,
    }
