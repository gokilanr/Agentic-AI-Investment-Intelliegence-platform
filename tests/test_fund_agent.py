
import numpy as np
import pandas as pd
import pytest

from agents.fund_agent import run_fund_agent


def make_fund_data(rows=260):
    dates = pd.date_range("2024-01-01", periods=rows, freq="B")
    close = np.linspace(100, 130, rows)

    return pd.DataFrame({
        "Date": dates,
        "Open": close - 0.5,
        "High": close + 1.0,
        "Low": close - 1.0,
        "Close": close,
        "Volume": np.full(rows, 10000),
    })


def test_run_fund_agent_returns_report(monkeypatch):
    monkeypatch.setattr(
        "agents.fund_agent.fetch_stock_data",
        lambda ticker, period: make_fund_data(),
    )

    monkeypatch.setattr(
        "agents.fund_agent.get_fund_profile",
        lambda ticker: {
            "ticker": ticker,
            "name": "Example Fund",
            "category": "Large Blend",
        },
    )

    monkeypatch.setattr(
        "agents.fund_agent.analyze_fund_intelligence",
        lambda data, fund_name, fund_type, risk_free_rate: {
            "fund": {"name": fund_name, "type": fund_type},
            "risk_classification": "moderate",
        },
    )

    result = run_fund_agent("SPY")

    assert result["status"] == "success"
    assert result["agent"] == "fund_agent"
    assert result["ticker"] == "SPY"
    assert result["profile"]["name"] == "Example Fund"
    assert result["analysis"]["risk_classification"] == "moderate"


def test_run_fund_agent_rejects_empty_ticker():
    with pytest.raises(ValueError, match="Ticker cannot be empty"):
        run_fund_agent(" ")


def test_run_fund_agent_rejects_invalid_risk_free_rate():
    with pytest.raises(ValueError, match="greater than -1"):
        run_fund_agent("SPY", risk_free_rate=-1.0)
