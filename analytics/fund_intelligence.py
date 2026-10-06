import numpy as np
import pandas as pd

from utils.logger import get_logger

logger = get_logger(__name__)


def calculate_fund_returns(
    data: pd.DataFrame
) -> dict:
    """
    Calculate historical fund/ETF return metrics.
    """

    if data.empty:
        return {
            "total_return": np.nan,
            "cagr": np.nan,
            "best_period": np.nan,
            "worst_period": np.nan,
        }

    prices = data["Close"].dropna()

    if len(prices) < 2:
        return {
            "total_return": np.nan,
            "cagr": np.nan,
            "best_period": np.nan,
            "worst_period": np.nan,
        }

    total_return = (
        prices.iloc[-1] / prices.iloc[0]
    ) - 1

    years = len(prices) / 252

    cagr = (
        (prices.iloc[-1] / prices.iloc[0])
        ** (1 / years)
    ) - 1

    returns = prices.pct_change().dropna()

    return {
        "total_return": total_return,
        "cagr": cagr,
        "best_period": returns.max(),
        "worst_period": returns.min(),
    }


def calculate_fund_risk(
    data: pd.DataFrame
) -> dict:
    """
    Calculate fund/ETF risk metrics.
    """

    prices = data["Close"].dropna()

    if len(prices) < 2:
        return {
            "annualized_volatility": np.nan,
            "max_drawdown": np.nan,
        }

    returns = prices.pct_change().dropna()

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


def calculate_fund_sharpe_ratio(
    data: pd.DataFrame,
    risk_free_rate: float = 0.0
) -> float:
    """
    Calculate annualized Sharpe ratio.
    """

    prices = data["Close"].dropna()

    if len(prices) < 2:
        return np.nan

    returns = prices.pct_change().dropna()

    daily_rf = (
        (1 + risk_free_rate) ** (1 / 252)
    ) - 1

    excess_returns = returns - daily_rf

    volatility = excess_returns.std()

    if volatility == 0:
        return np.nan

    return (
        excess_returns.mean()
        / volatility
    ) * np.sqrt(252)


def calculate_rolling_returns(
    data: pd.DataFrame
) -> dict:
    """
    Calculate rolling return metrics.
    """

    prices = data["Close"].dropna()

    if len(prices) < 252:
        return {
            "return_1m": np.nan,
            "return_3m": np.nan,
            "return_6m": np.nan,
            "return_1y": np.nan,
        }

    return {
        "return_1m": (
            prices.iloc[-1] / prices.iloc[-21]
        ) - 1,

        "return_3m": (
            prices.iloc[-1] / prices.iloc[-63]
        ) - 1,

        "return_6m": (
            prices.iloc[-1] / prices.iloc[-126]
        ) - 1,

        "return_1y": (
            prices.iloc[-1] / prices.iloc[-252]
        ) - 1,
    }


def calculate_downside_risk(
    data: pd.DataFrame
) -> dict:
    """
    Calculate downside deviation and Sortino ratio.
    """

    prices = data["Close"].dropna()

    if len(prices) < 2:
        return {
            "downside_deviation": np.nan,
            "sortino_ratio": np.nan,
        }

    returns = prices.pct_change().dropna()

    negative_returns = returns[returns < 0]

    if negative_returns.empty:
        return {
            "downside_deviation": 0.0,
            "sortino_ratio": np.nan,
        }

    downside_deviation = (
        negative_returns.std() * np.sqrt(252)
    )

    annualized_return = returns.mean() * 252

    if downside_deviation == 0:
        sortino_ratio = np.nan
    else:
        sortino_ratio = (
            annualized_return
            / downside_deviation
        )

    return {
        "downside_deviation": downside_deviation,
        "sortino_ratio": sortino_ratio,
    }


def classify_fund_risk(
    volatility: float
) -> str:
    """
    Classify risk based on annualized volatility.

    These thresholds are heuristic and should not
    be interpreted as regulatory risk categories.
    """

    if pd.isna(volatility):
        return "unknown"

    if volatility < 0.10:
        return "low"

    if volatility < 0.20:
        return "moderate"

    if volatility < 0.30:
        return "high"

    return "very_high"


def analyze_fund_intelligence(
    data: pd.DataFrame,
    fund_name: str,
    fund_type: str = "ETF",
    risk_free_rate: float = 0.0,
) -> dict:
    """
    Generate a complete mutual fund / ETF
    intelligence report.
    """

    logger.info(
        f"Starting fund intelligence analysis for {fund_name}."
    )

    returns = calculate_fund_returns(data)
    risk = calculate_fund_risk(data)

    sharpe_ratio = calculate_fund_sharpe_ratio(
        data,
        risk_free_rate
    )

    rolling_returns = calculate_rolling_returns(
        data
    )

    downside_risk = calculate_downside_risk(
        data
    )

    risk_classification = classify_fund_risk(
        risk["annualized_volatility"]
    )

    result = {
        "fund": {
            "name": fund_name,
            "type": fund_type,
        },
        "returns": returns,
        "risk": risk,
        "risk_adjusted": {
            "sharpe_ratio": sharpe_ratio,
            "sortino_ratio": downside_risk[
                "sortino_ratio"
            ],
        },
        "rolling_returns": rolling_returns,
        "downside_risk": downside_risk,
        "risk_classification": risk_classification,
    }

    logger.info(
        f"Fund intelligence analysis completed for {fund_name}."
    )

    return result