import numpy as np
import pandas as pd
import pytest

from analytics.stock_intelligence import (
    calculate_performance_metrics,
    calculate_risk_metrics,
    calculate_sharpe_ratio,
    classify_trend,
    analyze_stock_intelligence,
)


def create_test_data():

    close = np.linspace(
        100,
        120,
        252
    )

    data = pd.DataFrame({
        "Close": close,
        "Daily_Return": pd.Series(close).pct_change(),
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


def test_performance_metrics():

    data = create_test_data()

    result = calculate_performance_metrics(data)

    assert result["total_return"] == pytest.approx(
        0.20
    )

    assert result["best_day"] >= 0

    assert result["worst_day"] >= 0

    
def test_risk_metrics():

    data = create_test_data()

    result = calculate_risk_metrics(data)

    assert result["annualized_volatility"] >= 0
    assert result["max_drawdown"] <= 0


def test_sharpe_ratio():

    data = create_test_data()

    result = calculate_sharpe_ratio(data)

    assert np.isfinite(result)


def test_trend_classification():

    data = create_test_data()

    result = classify_trend(data)

    assert result == "mixed"


def test_stock_intelligence():

    data = create_test_data()

    result = analyze_stock_intelligence(
        data,
        "TEST"
    )

    assert result["ticker"] == "TEST"
    assert "performance" in result
    assert "risk" in result
    assert "trend" in result
    assert "momentum" in result
    assert "volume" in result
    assert "risk_adjusted" in result