
import numpy as np
import pandas as pd
import pytest

from agents.stock_agent import prepare_stock_data, run_stock_agent


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


def test_prepare_stock_data_creates_required_features():
    result = prepare_stock_data(make_market_data())

    assert "Daily_Return" in result.columns
    assert "SMA_200" in result.columns
    assert "Momentum_20" in result.columns
    assert "Volume_Ratio" in result.columns
    assert len(result) == 250


def test_prepare_stock_data_rejects_empty_data():
    with pytest.raises(ValueError, match="cannot be empty"):
        prepare_stock_data(pd.DataFrame())


def test_run_stock_agent_returns_report(monkeypatch):
    raw_data = make_market_data()

    monkeypatch.setattr(
        "agents.stock_agent.fetch_stock_data",
        lambda ticker, period: raw_data.copy(),
    )

    monkeypatch.setattr(
        "agents.stock_agent.analyze_stock_intelligence",
        lambda data, ticker, risk_free_rate: {
            "ticker": ticker,
            "trend_classification": "strong_uptrend",
        },
    )

    result = run_stock_agent("RELIANCE.NS")

    assert result["status"] == "success"
    assert result["ticker"] == "RELIANCE.NS"
    assert result["analysis"]["trend_classification"] == "strong_uptrend"


def test_run_stock_agent_rejects_empty_ticker():
    with pytest.raises(ValueError, match="Ticker cannot be empty"):
        run_stock_agent(" ")
