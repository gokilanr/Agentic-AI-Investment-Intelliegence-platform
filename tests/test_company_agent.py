
import numpy as np
import pandas as pd

from agents.company_agent import run_company_agent


def make_market_data(rows=250):
    dates = pd.date_range("2024-01-01", periods=rows, freq="B")
    close = np.linspace(100, 150, rows)

    return pd.DataFrame({
        "Date": dates,
        "Open": close - 0.5,
        "High": close + 1.0,
        "Low": close - 1.0,
        "Close": close,
        "Volume": np.full(rows, 10000),
    })


def test_run_company_agent_returns_company_report(monkeypatch):
    monkeypatch.setattr(
        "agents.company_agent.fetch_stock_data",
        lambda ticker, period: make_market_data(),
    )

    monkeypatch.setattr(
        "agents.company_agent.build_company_intelligence",
        lambda data, ticker, risk_free_rate: {
            "company": {
                "ticker": ticker,
                "company_name": "Reliance Industries Limited",
                "sector": "Energy",
            },
            "stock_analysis": {
                "ticker": ticker,
                "trend_classification": "strong_uptrend",
            },
        },
    )

    result = run_company_agent("RELIANCE.NS")

    assert result["status"] == "success"
    assert result["agent"] == "company_agent"
    assert result["ticker"] == "RELIANCE.NS"
    assert (
        result["analysis"]["company"]["company_name"]
        == "Reliance Industries Limited"
    )


def test_run_company_agent_rejects_empty_ticker():
    import pytest

    with pytest.raises(ValueError, match="Ticker cannot be empty"):
        run_company_agent(" ")
