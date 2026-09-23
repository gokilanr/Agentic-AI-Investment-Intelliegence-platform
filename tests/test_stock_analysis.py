import numpy as np
import pandas as pd
import pytest

from analytics.stock_analysis import (
    calculate_stock_performance,
    calculate_stock_risk,
    analyze_stock,
)


def create_test_data():
    dates = pd.date_range(
        "2026-01-01",
        periods=252,
        freq="D",
    )

    close = np.linspace(
        100,
        120,
        252,
    )

    daily_return = (
        pd.Series(close)
        .pct_change()
    )

    data = pd.DataFrame({
        "Date": dates,
        "Close": close,
        "Daily_Return": daily_return,
        "SMA_20": close,
        "SMA_50": close,
        "SMA_200": close,
        "Price_vs_SMA_20": 0.0,
        "Price_vs_SMA_50": 0.0,
        "Price_vs_SMA_200": 0.0,
        "Momentum_20": 0.0,
        "Momentum_50": 0.0,
        "ROC_20": 0.0,
        "ROC_50": 0.0,
        "Volume": 1000,
        "Volume_Change": 0.0,
        "Volume_SMA_20": 1000,
        "Volume_Ratio": 1.0,
    })

    return data


def test_calculate_stock_performance():

    data = create_test_data()

    result = calculate_stock_performance(
        data
    )

    assert result["current_price"] == pytest.approx(
        120
    )

    assert result["total_return"] == pytest.approx(
        0.20
    )


def test_calculate_stock_risk():

    data = create_test_data()

    result = calculate_stock_risk(
        data
    )

    assert result["daily_volatility"] >= 0

    assert result["annualized_volatility"] >= 0

    assert result["max_drawdown"] <= 0


def test_analyze_stock():

    data = create_test_data()

    result = analyze_stock(
        data,
        "TEST"
    )

    assert result["ticker"] == "TEST"

    assert "performance" in result
    assert "risk" in result
    assert "trend" in result
    assert "momentum" in result
    assert "volume" in result