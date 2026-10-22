
import pytest

from agents.bond_agent import run_bond_agent


def test_run_bond_agent_returns_analysis(monkeypatch):
    monkeypatch.setattr(
        "agents.bond_agent.build_bond_analysis",
        lambda **kwargs: {
            "profile": {"bond_id": kwargs["bond_id"]},
            "intelligence": {"ytm": 0.045},
        },
    )

    result = run_bond_agent(
        bond_id="BOND001",
        issuer="Example Corporation",
        bond_type="Corporate",
        price=98.0,
        coupon_rate=0.05,
        maturity_years=5,
        face_value=100,
        credit_rating="AA",
    )

    assert result["status"] == "success"
    assert result["agent"] == "bond_agent"
    assert result["bond_id"] == "BOND001"
    assert result["analysis"]["intelligence"]["ytm"] == 0.045


def test_run_bond_agent_rejects_invalid_price():
    with pytest.raises(ValueError, match="Bond price"):
        run_bond_agent(
            bond_id="BOND001",
            issuer="Example Corporation",
            bond_type="Corporate",
            price=0,
            coupon_rate=0.05,
            maturity_years=5,
        )


def test_run_bond_agent_rejects_invalid_coupon_rate():
    with pytest.raises(ValueError, match="Coupon rate"):
        run_bond_agent(
            bond_id="BOND001",
            issuer="Example Corporation",
            bond_type="Corporate",
            price=98,
            coupon_rate=5.0,
            maturity_years=5,
        )


def test_run_bond_agent_rejects_invalid_frequency():
    with pytest.raises(ValueError, match="Frequency"):
        run_bond_agent(
            bond_id="BOND001",
            issuer="Example Corporation",
            bond_type="Corporate",
            price=98,
            coupon_rate=0.05,
            maturity_years=5,
            frequency=0,
        )
