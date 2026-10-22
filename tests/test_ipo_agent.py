
import pytest

from agents.ipo_agent import run_ipo_agent


@pytest.fixture
def valid_ipo_inputs():
    return {
        "ipo_id": "IPO001",
        "company_name": "Example Technologies",
        "sector": "Technology",
        "exchange": "NSE",
        "issue_price": 150.0,
        "issue_size": 500.0,
        "lot_size": 90,
        "revenue_growth": 0.20,
        "profit_growth": 0.15,
        "net_margin": 0.12,
        "debt_to_equity": 0.30,
        "pe_ratio": 25.0,
        "subscription_ratio": 12.5,
        "listing_price": 180.0,
        "fresh_issue_percentage": 70.0,
        "ofs_percentage": 30.0,
        "promoter_holding": 55.0,
    }


def test_run_ipo_agent_returns_analysis(monkeypatch, valid_ipo_inputs):
    def mock_build_ipo_analysis(**kwargs):
        return {
            "profile": {"ipo_id": kwargs["ipo_id"]},
            "intelligence": {"recommendation": "Review further"},
        }

    monkeypatch.setattr(
        "agents.ipo_agent.build_ipo_analysis",
        mock_build_ipo_analysis,
    )

    result = run_ipo_agent(**valid_ipo_inputs)

    assert result["agent"] == "ipo_agent"
    assert result["status"] == "success"
    assert result["ipo_id"] == "IPO001"
    assert result["analysis"]["intelligence"]["recommendation"] == "Review further"


def test_run_ipo_agent_rejects_empty_company_name(valid_ipo_inputs):
    valid_ipo_inputs["company_name"] = "   "

    with pytest.raises(ValueError, match="Company name"):
        run_ipo_agent(**valid_ipo_inputs)


def test_run_ipo_agent_rejects_invalid_issue_price(valid_ipo_inputs):
    valid_ipo_inputs["issue_price"] = 0

    with pytest.raises(ValueError, match="Issue price"):
        run_ipo_agent(**valid_ipo_inputs)


def test_run_ipo_agent_rejects_invalid_subscription_ratio(valid_ipo_inputs):
    valid_ipo_inputs["subscription_ratio"] = -1

    with pytest.raises(ValueError, match="Subscription ratio"):
        run_ipo_agent(**valid_ipo_inputs)


def test_run_ipo_agent_rejects_invalid_percentage(valid_ipo_inputs):
    valid_ipo_inputs["promoter_holding"] = 120

    with pytest.raises(ValueError, match="Promoter holding"):
        run_ipo_agent(**valid_ipo_inputs)
