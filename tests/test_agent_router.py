
import pytest

from agents.agent_router import route_investment_request


def test_routes_stock_request(monkeypatch):
    def mock_stock_agent(**kwargs):
        return {"ticker": kwargs["ticker"], "analysis": "stock result"}

    monkeypatch.setattr("agents.agent_router.run_stock_agent", mock_stock_agent)

    result = route_investment_request(
        " STOCK ",
        {"ticker": "RELIANCE.NS", "period": "1y"},
    )

    assert result["status"] == "success"
    assert result["investment_type"] == "stock"
    assert result["result"]["ticker"] == "RELIANCE.NS"


def test_routes_ipo_request(monkeypatch):
    def mock_ipo_agent(**kwargs):
        return {"ipo_id": kwargs["ipo_id"]}

    monkeypatch.setattr("agents.agent_router.run_ipo_agent", mock_ipo_agent)

    result = route_investment_request("ipo", {"ipo_id": "IPO001"})

    assert result["status"] == "success"
    assert result["investment_type"] == "ipo"
    assert result["result"]["ipo_id"] == "IPO001"


def test_rejects_empty_investment_type():
    with pytest.raises(ValueError, match="Investment type"):
        route_investment_request("", {})


def test_rejects_non_dictionary_parameters():
    with pytest.raises(ValueError, match="dictionary"):
        route_investment_request("stock", "RELIANCE.NS")


def test_rejects_unsupported_investment_type():
    with pytest.raises(ValueError, match="Unsupported investment type"):
        route_investment_request("crypto", {})


def test_propagates_agent_errors(monkeypatch):
    def mock_stock_agent(**kwargs):
        raise ValueError("Invalid ticker")

    monkeypatch.setattr("agents.agent_router.run_stock_agent", mock_stock_agent)

    with pytest.raises(ValueError, match="Invalid ticker"):
        route_investment_request("stock", {"ticker": "INVALID"})
