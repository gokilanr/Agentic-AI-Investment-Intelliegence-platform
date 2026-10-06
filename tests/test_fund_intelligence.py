import numpy as np
import pandas as pd
import pytest

from analytics.fund_intelligence import (
    calculate_fund_returns,
    calculate_fund_risk,
    calculate_fund_sharpe_ratio,
    calculate_rolling_returns,
    calculate_downside_risk,
    classify_fund_risk,
    analyze_fund_intelligence,
)


def create_test_data():

    close = np.linspace(
        100,
        150,
        300
    )

    return pd.DataFrame({
        "Close": close
    })


def test_fund_returns():

    data = create_test_data()

    result = calculate_fund_returns(data)

    assert result["total_return"] == pytest.approx(
        0.50
    )

    assert np.isfinite(
        result["cagr"]
    )

    assert result["best_period"] > 0


def test_fund_risk():

    data = create_test_data()

    result = calculate_fund_risk(data)

    assert result[
        "annualized_volatility"
    ] >= 0

    assert result[
        "max_drawdown"
    ] <= 0


def test_sharpe_ratio():

    data = create_test_data()

    result = calculate_fund_sharpe_ratio(data)

    assert np.isfinite(result)


def test_rolling_returns():

    data = create_test_data()

    result = calculate_rolling_returns(data)

    assert np.isfinite(
        result["return_1m"]
    )

    assert np.isfinite(
        result["return_1y"]
    )


def test_downside_risk():

    data = create_test_data()

    result = calculate_downside_risk(data)

    assert (
        result["downside_deviation"] >= 0
    )


def test_risk_classification():

    assert classify_fund_risk(0.05) == "low"
    assert classify_fund_risk(0.15) == "moderate"
    assert classify_fund_risk(0.25) == "high"
    assert classify_fund_risk(0.35) == "very_high"


def test_complete_fund_intelligence():

    data = create_test_data()

    result = analyze_fund_intelligence(
        data,
        "TEST ETF",
        "ETF"
    )

    assert result["fund"]["name"] == "TEST ETF"
    assert result["fund"]["type"] == "ETF"

    assert "returns" in result
    assert "risk" in result
    assert "risk_adjusted" in result
    assert "rolling_returns" in result
    assert "downside_risk" in result
    assert "risk_classification" in result