import pandas as pd
import pytest

from analytics.fundamental_analysis import (
    calculate_growth_metrics,
    calculate_profitability_metrics,
    calculate_financial_health,
    calculate_cash_flow_metrics,
    analyze_fundamentals,
)


def create_financial_test_data():

    return pd.DataFrame({
        "Revenue": [
            1000,
            1200,
        ],
        "Net_Income": [
            100,
            150,
        ],
        "Total_Assets": [
            2000,
            2500,
        ],
        "Total_Equity": [
            1000,
            1250,
        ],
        "Total_Debt": [
            500,
            600,
        ],
        "Current_Assets": [
            800,
            1000,
        ],
        "Current_Liabilities": [
            400,
            500,
        ],
        "Operating_Cash_Flow": [
            200,
            300,
        ],
        "Capital_Expenditure": [
            -80,
            -100,
        ],
    })


def test_calculate_growth_metrics():

    data = create_financial_test_data()

    result = calculate_growth_metrics(data)

    assert result["revenue_growth"] == pytest.approx(
        0.20
    )

    assert result["earnings_growth"] == pytest.approx(
        0.50
    )


def test_calculate_profitability_metrics():

    data = create_financial_test_data()

    result = calculate_profitability_metrics(data)

    assert result["net_margin"] == pytest.approx(
        0.125
    )

    assert result["roa"] == pytest.approx(
        0.06
    )

    assert result["roe"] == pytest.approx(
        0.12
    )


def test_calculate_financial_health():

    data = create_financial_test_data()

    result = calculate_financial_health(data)

    assert result["debt_to_equity"] == pytest.approx(
        0.48
    )

    assert result["current_ratio"] == pytest.approx(
        2.0
    )


def test_calculate_cash_flow_metrics():

    data = create_financial_test_data()

    result = calculate_cash_flow_metrics(data)

    assert result["free_cash_flow"] == pytest.approx(
        200
    )


def test_analyze_fundamentals():

    data = create_financial_test_data()

    result = analyze_fundamentals(
        data,
        "TEST"
    )

    assert result["ticker"] == "TEST"

    assert "growth" in result
    assert "profitability" in result
    assert "financial_health" in result
    assert "cash_flow" in result