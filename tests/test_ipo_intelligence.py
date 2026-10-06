import pytest

from analytics.ipo_intelligence import (
    calculate_listing_gain,
    calculate_subscription_score,
    calculate_growth_score,
    calculate_profitability_score,
    calculate_leverage_score,
    calculate_valuation_score,
    calculate_ipo_score,
    classify_ipo_score,
    analyze_ipo_intelligence,
)

from analytics.ipo_profile import (
    create_ipo_profile,
)

from analytics.ipo_analysis import (
    build_ipo_analysis,
)


def test_listing_gain():

    result = calculate_listing_gain(
        issue_price=100,
        listing_price=120,
    )

    assert result == pytest.approx(0.20)


def test_subscription_score():

    assert calculate_subscription_score(0.5) == 20
    assert calculate_subscription_score(3) == 60
    assert calculate_subscription_score(15) == 100


def test_growth_score():

    result = calculate_growth_score(
        revenue_growth=0.20,
        profit_growth=0.30,
    )

    assert result == pytest.approx(25.0)


def test_profitability_score():

    assert calculate_profitability_score(
        0.03
    ) == 25

    assert calculate_profitability_score(
        0.15
    ) == 75


def test_leverage_score():

    assert calculate_leverage_score(
        0.20
    ) == 100

    assert calculate_leverage_score(
        1.50
    ) == 40


def test_valuation_score():

    assert calculate_valuation_score(
        12
    ) == 100

    assert calculate_valuation_score(
        50
    ) == 40


def test_ipo_score():

    result = calculate_ipo_score(
        subscription_score=80,
        growth_score=80,
        profitability_score=80,
        leverage_score=80,
        valuation_score=80,
    )

    assert result == 80


def test_ipo_classification():

    assert classify_ipo_score(85) == "strong"
    assert classify_ipo_score(70) == "positive"
    assert classify_ipo_score(55) == "neutral"
    assert classify_ipo_score(40) == "weak"
    assert classify_ipo_score(20) == "high_risk"


def test_ipo_profile():

    result = create_ipo_profile(
        ipo_id="TEST-IPO",
        company_name="Test Technologies",
        sector="Technology",
        exchange="NSE",
        issue_price=100,
        issue_size=500,
        lot_size=15,
    )

    assert result["ipo_id"] == "TEST-IPO"
    assert result["company_name"] == (
        "Test Technologies"
    )
    assert result["lot_size"] == 15


def test_complete_ipo_intelligence():

    result = analyze_ipo_intelligence(
        company_name="Test Technologies",
        issue_price=100,
        issue_size=500,
        revenue_growth=0.20,
        profit_growth=0.25,
        net_margin=0.15,
        debt_to_equity=0.40,
        pe_ratio=20,
        subscription_ratio=8,
        listing_price=125,
    )

    assert result["company"] == (
        "Test Technologies"
    )

    assert "ipo_details" in result
    assert "market_demand" in result
    assert "fundamentals" in result
    assert "scores" in result
    assert "listing" in result

    assert result["listing"]["listing_gain"] == (
        pytest.approx(0.25)
    )

    assert result["scores"]["overall_score"] > 0


def test_complete_ipo_analysis():

    result = build_ipo_analysis(
        ipo_id="TEST-IPO",
        company_name="Test Technologies",
        sector="Technology",
        exchange="NSE",
        issue_price=100,
        issue_size=500,
        lot_size=15,
        revenue_growth=0.20,
        profit_growth=0.25,
        net_margin=0.15,
        debt_to_equity=0.40,
        pe_ratio=20,
        subscription_ratio=8,
        listing_price=125,
    )

    assert "profile" in result
    assert "intelligence" in result

    assert (
        result["profile"]["company_name"]
        == "Test Technologies"
    )