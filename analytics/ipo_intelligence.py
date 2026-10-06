import numpy as np

from utils.logger import get_logger


logger = get_logger(__name__)


def calculate_listing_gain(
    issue_price: float,
    listing_price: float,
) -> float:
    """
    Calculate IPO listing gain/loss.
    """

    if issue_price <= 0:
        raise ValueError(
            "Issue price must be greater than zero."
        )

    return (
        listing_price / issue_price
    ) - 1


def calculate_subscription_score(
    subscription_ratio: float,
) -> float:
    """
    Convert subscription ratio into a normalized
    score between 0 and 100.

    This is an InvestIQ analytical heuristic,
    not an official IPO rating.
    """

    if subscription_ratio < 0:
        raise ValueError(
            "Subscription ratio cannot be negative."
        )

    if subscription_ratio < 1:
        return 20.0

    if subscription_ratio < 2:
        return 40.0

    if subscription_ratio < 5:
        return 60.0

    if subscription_ratio < 10:
        return 80.0

    return 100.0


def calculate_growth_score(
    revenue_growth: float,
    profit_growth: float,
) -> float:
    """
    Score revenue and profit growth.
    """

    revenue_score = min(
        max(revenue_growth * 100, 0),
        100,
    )

    profit_score = min(
        max(profit_growth * 100, 0),
        100,
    )

    return (
        revenue_score * 0.5
        + profit_score * 0.5
    )


def calculate_profitability_score(
    net_margin: float,
) -> float:
    """
    Score profitability based on net margin.
    """

    if net_margin < 0:
        return 0.0

    if net_margin < 0.05:
        return 25.0

    if net_margin < 0.10:
        return 50.0

    if net_margin < 0.20:
        return 75.0

    return 100.0


def calculate_leverage_score(
    debt_to_equity: float,
) -> float:
    """
    Lower leverage receives a higher score.
    """

    if debt_to_equity < 0:
        raise ValueError(
            "Debt-to-equity cannot be negative."
        )

    if debt_to_equity <= 0.25:
        return 100.0

    if debt_to_equity <= 0.50:
        return 80.0

    if debt_to_equity <= 1.00:
        return 60.0

    if debt_to_equity <= 2.00:
        return 40.0

    return 20.0


def calculate_valuation_score(
    pe_ratio: float,
) -> float:
    """
    Heuristic valuation score.

    Lower P/E receives a higher score.
    """

    if pe_ratio <= 0:
        return 0.0

    if pe_ratio <= 15:
        return 100.0

    if pe_ratio <= 25:
        return 80.0

    if pe_ratio <= 40:
        return 60.0

    if pe_ratio <= 60:
        return 40.0

    return 20.0


def calculate_ipo_score(
    subscription_score: float,
    growth_score: float,
    profitability_score: float,
    leverage_score: float,
    valuation_score: float,
) -> float:
    """
    Calculate weighted IPO attractiveness score.
    """

    score = (
        subscription_score * 0.15
        + growth_score * 0.25
        + profitability_score * 0.20
        + leverage_score * 0.20
        + valuation_score * 0.20
    )

    return round(score, 2)


def classify_ipo_score(
    score: float,
) -> str:
    """
    Convert IPO score into an analytical classification.
    """

    if score >= 80:
        return "strong"

    if score >= 65:
        return "positive"

    if score >= 50:
        return "neutral"

    if score >= 35:
        return "weak"

    return "high_risk"


def calculate_listing_price_metrics(
    issue_price: float,
    listing_price: float | None = None,
) -> dict:
    """
    Calculate listing performance if listing price
    is available.
    """

    if issue_price <= 0:
        raise ValueError(
            "Issue price must be greater than zero."
        )

    if listing_price is None:
        return {
            "listing_price": None,
            "listing_gain": None,
        }

    if listing_price <= 0:
        raise ValueError(
            "Listing price must be greater than zero."
        )

    listing_gain = calculate_listing_gain(
        issue_price,
        listing_price,
    )

    return {
        "listing_price": listing_price,
        "listing_gain": listing_gain,
    }


def analyze_ipo_intelligence(
    company_name: str,
    issue_price: float,
    issue_size: float,
    revenue_growth: float,
    profit_growth: float,
    net_margin: float,
    debt_to_equity: float,
    pe_ratio: float,
    subscription_ratio: float,
    listing_price: float | None = None,
    fresh_issue_percentage: float | None = None,
    promoter_holding: float | None = None,
) -> dict:
    """
    Generate complete IPO intelligence report.
    """

    logger.info(
        f"Starting IPO intelligence analysis for "
        f"{company_name}."
    )

    subscription_score = (
        calculate_subscription_score(
            subscription_ratio
        )
    )

    growth_score = calculate_growth_score(
        revenue_growth,
        profit_growth,
    )

    profitability_score = (
        calculate_profitability_score(
            net_margin
        )
    )

    leverage_score = calculate_leverage_score(
        debt_to_equity
    )

    valuation_score = calculate_valuation_score(
        pe_ratio
    )

    overall_score = calculate_ipo_score(
        subscription_score=subscription_score,
        growth_score=growth_score,
        profitability_score=profitability_score,
        leverage_score=leverage_score,
        valuation_score=valuation_score,
    )

    classification = classify_ipo_score(
        overall_score
    )

    listing_metrics = (
        calculate_listing_price_metrics(
            issue_price,
            listing_price,
        )
    )

    result = {
        "company": company_name,

        "ipo_details": {
            "issue_price": issue_price,
            "issue_size": issue_size,
            "fresh_issue_percentage":
                fresh_issue_percentage,
            "promoter_holding":
                promoter_holding,
        },

        "market_demand": {
            "subscription_ratio":
                subscription_ratio,
            "subscription_score":
                subscription_score,
        },

        "fundamentals": {
            "revenue_growth":
                revenue_growth,
            "profit_growth":
                profit_growth,
            "net_margin":
                net_margin,
            "debt_to_equity":
                debt_to_equity,
            "pe_ratio":
                pe_ratio,
        },

        "scores": {
            "growth_score":
                growth_score,
            "profitability_score":
                profitability_score,
            "leverage_score":
                leverage_score,
            "valuation_score":
                valuation_score,
            "overall_score":
                overall_score,
        },

        "listing": listing_metrics,

        "classification": classification,
    }

    logger.info(
        f"IPO intelligence analysis completed for "
        f"{company_name}."
    )

    return result