import pytest

from analytics.bond_intelligence import (
    calculate_current_yield,
    calculate_ytm,
    calculate_macaulay_duration,
    calculate_modified_duration,
    calculate_price_sensitivity,
    calculate_accrued_interest,
    classify_credit_risk,
    classify_interest_rate_risk,
    analyze_bond_intelligence,
)

from analytics.bond_profile import (
    create_bond_profile,
)

from analytics.bond_analysis import (
    build_bond_analysis,
)


def test_current_yield():

    result = calculate_current_yield(
        price=95,
        coupon_rate=0.08,
        face_value=100,
    )

    assert result == pytest.approx(
        0.0842105,
        rel=1e-4,
    )


def test_ytm():

    result = calculate_ytm(
        price=95,
        coupon_rate=0.08,
        face_value=100,
        years_to_maturity=5,
        frequency=2,
    )

    assert result > 0.08


def test_duration():

    ytm = calculate_ytm(
        price=95,
        coupon_rate=0.08,
        face_value=100,
        years_to_maturity=5,
    )

    duration = calculate_macaulay_duration(
        price=95,
        coupon_rate=0.08,
        face_value=100,
        years_to_maturity=5,
        ytm=ytm,
    )

    modified = calculate_modified_duration(
        duration,
        ytm,
    )

    assert duration > 0
    assert modified > 0
    assert modified < duration


def test_price_sensitivity():

    result = calculate_price_sensitivity(
        modified_duration=4,
        yield_change=0.01,
    )

    assert result == pytest.approx(
        -0.04
    )


def test_accrued_interest():

    result = calculate_accrued_interest(
        face_value=100,
        coupon_rate=0.08,
        days_since_coupon=90,
        coupon_period_days=180,
    )

    assert result == pytest.approx(
        4.0
    )


def test_credit_risk():

    assert classify_credit_risk(
        "AAA"
    ) == "very_low"

    assert classify_credit_risk(
        "AA"
    ) == "low"

    assert classify_credit_risk(
        "A"
    ) == "moderate"

    assert classify_credit_risk(
        "BBB"
    ) == "medium_high"

    assert classify_credit_risk(
        "B"
    ) == "high"


def test_interest_rate_risk():

    assert classify_interest_rate_risk(
        1.5
    ) == "low"

    assert classify_interest_rate_risk(
        4
    ) == "moderate"

    assert classify_interest_rate_risk(
        6
    ) == "high"

    assert classify_interest_rate_risk(
        10
    ) == "very_high"


def test_bond_profile():

    result = create_bond_profile(
        bond_id="TEST001",
        issuer="Test Corporation",
        bond_type="Corporate",
        coupon_rate=0.08,
        maturity_years=5,
        face_value=100,
        credit_rating="AA",
    )

    assert result["bond_id"] == "TEST001"
    assert result["issuer"] == "Test Corporation"
    assert result["coupon_rate"] == 0.08


def test_complete_bond_intelligence():

    result = analyze_bond_intelligence(
        price=95,
        coupon_rate=0.08,
        face_value=100,
        years_to_maturity=5,
        credit_rating="AA",
    )

    assert "valuation" in result
    assert "duration" in result
    assert "interest_rate_risk" in result
    assert "credit_risk" in result

    assert result["valuation"]["ytm"] > 0
    assert result["duration"][
        "modified_duration"
    ] > 0


def test_complete_bond_analysis():

    result = build_bond_analysis(
        bond_id="TEST001",
        issuer="Test Corporation",
        bond_type="Corporate",
        price=95,
        coupon_rate=0.08,
        maturity_years=5,
        credit_rating="AA",
    )

    assert "profile" in result
    assert "intelligence" in result

    assert (
        result["profile"]["issuer"]
        == "Test Corporation"
    )


def test_convexity():

    result = analyze_bond_intelligence(
        price=95,
        coupon_rate=0.08,
        face_value=100,
        years_to_maturity=5,
        credit_rating="AA",
    )

    assert result["duration"]["convexity"] > 0