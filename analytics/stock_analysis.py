import pandas as pd
import numpy as np

from utils.logger import get_logger

logger = get_logger(__name__)


def calculate_stock_performance(
    data: pd.DataFrame
) -> dict:
    """
    Calculate basic stock performance metrics.
    """

    logger.info("Calculating stock performance metrics.")

    close = data["Close"]

    current_price = close.iloc[-1]

    start_price = close.iloc[0]

    total_return = (
        current_price / start_price
    ) - 1

    trading_days = len(data)

    if trading_days > 1:
        annualized_return = (
            (current_price / start_price)
            ** (252 / trading_days)
        ) - 1
    else:
        annualized_return = np.nan

    result = {
        "current_price": current_price,
        "total_return": total_return,
        "annualized_return": annualized_return,
    }

    logger.info(
        "Stock performance calculation completed."
    )

    return result

def calculate_stock_risk(
    data: pd.DataFrame
) -> dict:
    """
    Calculate stock risk metrics.
    """

    logger.info("Calculating stock risk metrics.")

    daily_returns = data["Daily_Return"].dropna()

    if daily_returns.empty:
        return {
            "daily_volatility": np.nan,
            "annualized_volatility": np.nan,
            "max_drawdown": np.nan,
        }

    daily_volatility = daily_returns.std()

    annualized_volatility = (
        daily_volatility * np.sqrt(252)
    )

    cumulative_returns = (
        1 + daily_returns
    ).cumprod()

    running_max = cumulative_returns.cummax()

    drawdown = (
        cumulative_returns / running_max
    ) - 1

    max_drawdown = drawdown.min()

    result = {
        "daily_volatility": daily_volatility,
        "annualized_volatility": annualized_volatility,
        "max_drawdown": max_drawdown,
    }

    logger.info(
        "Stock risk calculation completed."
    )

    return result

def calculate_stock_trend(
    data: pd.DataFrame
) -> dict:
    """
    Calculate trend-related stock metrics.
    """

    logger.info("Calculating stock trend metrics.")

    latest = data.iloc[-1]

    result = {
        "price": latest["Close"],
        "sma_20": latest["SMA_20"],
        "sma_50": latest["SMA_50"],
        "sma_200": latest["SMA_200"],
        "price_vs_sma_20": latest["Price_vs_SMA_20"],
        "price_vs_sma_50": latest["Price_vs_SMA_50"],
        "price_vs_sma_200": latest["Price_vs_SMA_200"],
    }

    return result

def calculate_stock_momentum(
    data: pd.DataFrame
) -> dict:
    """
    Calculate momentum-related metrics.
    """

    logger.info("Calculating stock momentum metrics.")

    latest = data.iloc[-1]

    result = {
        "momentum_20": latest["Momentum_20"],
        "momentum_50": latest["Momentum_50"],
        "roc_20": latest["ROC_20"],
        "roc_50": latest["ROC_50"],
    }

    return result

def calculate_stock_volume(
    data: pd.DataFrame
) -> dict:
    """
    Calculate volume-related metrics.
    """

    logger.info("Calculating stock volume metrics.")

    latest = data.iloc[-1]

    result = {
        "volume": latest["Volume"],
        "volume_change": latest["Volume_Change"],
        "volume_sma_20": latest["Volume_SMA_20"],
        "volume_ratio": latest["Volume_Ratio"],
    }

    return result


def analyze_stock(
    data: pd.DataFrame,
    ticker: str
) -> dict:
    """
    Generate a complete stock analysis.
    """

    logger.info(
        f"Starting stock analysis for {ticker}."
    )

    performance = calculate_stock_performance(
        data
    )

    risk = calculate_stock_risk(
        data
    )

    trend = calculate_stock_trend(
        data
    )

    momentum = calculate_stock_momentum(
        data
    )

    volume = calculate_stock_volume(
        data
    )

    analysis = {
        "ticker": ticker,
        "performance": performance,
        "risk": risk,
        "trend": trend,
        "momentum": momentum,
        "volume": volume,
    }

    logger.info(
        f"Stock analysis completed for {ticker}."
    )

    return analysis