import pandas as pd
import numpy as np

from utils.logger import get_logger

logger = get_logger(__name__)


def calculate_performance_metrics(
    data: pd.DataFrame
) -> dict:
    """Calculate historical performance metrics."""

    returns = data["Daily_Return"].dropna()

    if returns.empty:
        return {
            "total_return": np.nan,
            "annualized_return": np.nan,
            "best_day": np.nan,
            "worst_day": np.nan,
        }

    start_price = data["Close"].iloc[0]
    current_price = data["Close"].iloc[-1]

    total_return = (
        current_price / start_price
    ) - 1

    trading_days = len(data)

    annualized_return = (
        (current_price / start_price)
        ** (252 / trading_days)
    ) - 1

    return {
        "total_return": total_return,
        "annualized_return": annualized_return,
        "best_day": returns.max(),
        "worst_day": returns.min(),
    }


def calculate_risk_metrics(
    data: pd.DataFrame
) -> dict:
    """Calculate stock risk metrics."""

    returns = data["Daily_Return"].dropna()

    if returns.empty:
        return {
            "annualized_volatility": np.nan,
            "max_drawdown": np.nan,
        }

    annualized_volatility = (
        returns.std() * np.sqrt(252)
    )

    cumulative_returns = (
        1 + returns
    ).cumprod()

    running_max = cumulative_returns.cummax()

    drawdown = (
        cumulative_returns / running_max
    ) - 1

    max_drawdown = drawdown.min()

    return {
        "annualized_volatility": annualized_volatility,
        "max_drawdown": max_drawdown,
    }


def calculate_trend_metrics(
    data: pd.DataFrame
) -> dict:
    """Calculate current trend metrics."""

    latest = data.iloc[-1]

    return {
        "current_price": latest["Close"],
        "sma_20": latest["SMA_20"],
        "sma_50": latest["SMA_50"],
        "sma_200": latest["SMA_200"],
        "price_vs_sma_20": latest["Price_vs_SMA_20"],
        "price_vs_sma_50": latest["Price_vs_SMA_50"],
        "price_vs_sma_200": latest["Price_vs_SMA_200"],
    }


def calculate_momentum_metrics(
    data: pd.DataFrame
) -> dict:
    """Calculate momentum metrics."""

    latest = data.iloc[-1]

    return {
        "momentum_20": latest["Momentum_20"],
        "momentum_50": latest["Momentum_50"],
        "roc_20": latest["ROC_20"],
        "roc_50": latest["ROC_50"],
    }


def calculate_volume_metrics(
    data: pd.DataFrame
) -> dict:
    """Calculate trading-volume metrics."""

    latest = data.iloc[-1]

    return {
        "volume": latest["Volume"],
        "volume_change": latest["Volume_Change"],
        "volume_sma_20": latest["Volume_SMA_20"],
        "volume_ratio": latest["Volume_Ratio"],
    }

def calculate_sharpe_ratio(
    data: pd.DataFrame,
    risk_free_rate: float = 0.0
) -> float:
    """
    Calculate annualized Sharpe ratio.

    Assumes risk_free_rate is an annual rate.
    """

    returns = data["Daily_Return"].dropna()

    if returns.empty:
        return np.nan

    daily_rf = (
        (1 + risk_free_rate) ** (1 / 252)
    ) - 1

    excess_returns = returns - daily_rf

    volatility = excess_returns.std()

    if volatility == 0:
        return np.nan

    sharpe_ratio = (
        excess_returns.mean()
        / volatility
    ) * np.sqrt(252)

    return sharpe_ratio

def classify_trend(
    data: pd.DataFrame
) -> str:
    """
    Classify the current price trend using
    SMA relationships.
    """

    latest = data.iloc[-1]

    price = latest["Close"]
    sma_20 = latest["SMA_20"]
    sma_50 = latest["SMA_50"]
    sma_200 = latest["SMA_200"]

    if pd.isna(sma_200):
        return "insufficient_data"

    if (
        price > sma_20
        and sma_20 > sma_50
        and sma_50 > sma_200
    ):
        return "strong_uptrend"

    if (
        price < sma_20
        and sma_20 < sma_50
        and sma_50 < sma_200
    ):
        return "strong_downtrend"

    if price > sma_200:
        return "above_long_term_trend"

    if price < sma_200:
        return "below_long_term_trend"

    return "mixed"


def analyze_stock_intelligence(
    data: pd.DataFrame,
    ticker: str,
    risk_free_rate: float = 0.0
) -> dict:
    """
    Generate a complete stock intelligence report.
    """

    logger.info(
        f"Starting stock intelligence analysis for {ticker}."
    )

    performance = calculate_performance_metrics(
        data
    )

    risk = calculate_risk_metrics(
        data
    )

    trend = calculate_trend_metrics(
        data
    )

    momentum = calculate_momentum_metrics(
        data
    )

    volume = calculate_volume_metrics(
        data
    )

    sharpe_ratio = calculate_sharpe_ratio(
        data,
        risk_free_rate
    )

    trend_classification = classify_trend(
        data
    )

    result = {
        "ticker": ticker,
        "performance": performance,
        "risk": risk,
        "trend": trend,
        "momentum": momentum,
        "volume": volume,
        "risk_adjusted": {
            "sharpe_ratio": sharpe_ratio
        },
        "trend_classification": trend_classification,
    }

    logger.info(
        f"Stock intelligence analysis completed for {ticker}."
    )

    return result