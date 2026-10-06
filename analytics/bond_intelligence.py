import numpy as np

from utils.logger import get_logger

logger = get_logger(__name__)


def calculate_current_yield(
    price: float,
    coupon_rate: float,
    face_value: float = 100.0,
) -> float:
    """
    Current yield = annual coupon / market price.
    """

    if price <= 0:
        raise ValueError("Bond price must be greater than zero.")

    annual_coupon = face_value * coupon_rate

    return annual_coupon / price


def calculate_ytm(
    price: float,
    coupon_rate: float,
    face_value: float,
    years_to_maturity: float,
    frequency: int = 2,
    tolerance: float = 1e-8,
    max_iterations: int = 100,
) -> float:
    """
    Calculate approximate Yield to Maturity using
    Newton-Raphson iteration.

    coupon_rate is expressed as a decimal.
    Example: 7.5% = 0.075.
    """

    if price <= 0:
        raise ValueError("Bond price must be greater than zero.")

    if face_value <= 0:
        raise ValueError("Face value must be greater than zero.")

    if years_to_maturity <= 0:
        raise ValueError(
            "Years to maturity must be greater than zero."
        )

    if frequency <= 0:
        raise ValueError(
            "Coupon frequency must be greater than zero."
        )

    periods = int(round(
        years_to_maturity * frequency
    ))

    if periods <= 0:
        raise ValueError(
            "Bond must have at least one coupon period."
        )

    coupon = (
        face_value
        * coupon_rate
        / frequency
    )

    # Initial YTM estimate using current yield.
    yield_rate = (
        (face_value * coupon_rate) / price
    )

    for _ in range(max_iterations):

        denominator = (
            1 + yield_rate / frequency
        )

        if denominator <= 0:
            yield_rate = 0.05
            denominator = (
                1 + yield_rate / frequency
            )

        price_estimate = (
            sum(
                coupon
                / denominator ** t
                for t in range(1, periods + 1)
            )
            + face_value
            / denominator ** periods
        )

        derivative = (
            sum(
                -t
                * coupon
                / frequency
                / denominator ** (t + 1)
                for t in range(1, periods + 1)
            )
            - (
                periods
                * face_value
                / frequency
                / denominator ** (periods + 1)
            )
        )

        if abs(derivative) < 1e-14:
            break

        adjustment = (
            price_estimate - price
        ) / derivative

        yield_rate -= adjustment

        if abs(adjustment) < tolerance:
            break

    return yield_rate


def calculate_macaulay_duration(
    price: float,
    coupon_rate: float,
    face_value: float,
    years_to_maturity: float,
    ytm: float,
    frequency: int = 2,
) -> float:
    """
    Calculate Macaulay duration in years.
    """

    if price <= 0:
        raise ValueError("Price must be greater than zero.")

    periods = int(round(
        years_to_maturity * frequency
    ))

    coupon = (
        face_value
        * coupon_rate
        / frequency
    )

    periodic_yield = ytm / frequency

    if 1 + periodic_yield <= 0:
        raise ValueError("Invalid YTM.")

    cash_flows = []

    for period in range(1, periods + 1):

        cash_flow = coupon

        if period == periods:
            cash_flow += face_value

        discounted_cash_flow = (
            cash_flow
            / (1 + periodic_yield) ** period
        )

        cash_flows.append(
            (period, discounted_cash_flow)
        )

    weighted_cash_flows = sum(
        period * discounted_cash_flow
        for period, discounted_cash_flow
        in cash_flows
    )

    present_value = sum(
        discounted_cash_flow
        for _, discounted_cash_flow
        in cash_flows
    )

    if present_value <= 0:
        raise ValueError(
            "Unable to calculate duration."
        )

    duration_periods = (
        weighted_cash_flows / present_value
    )

    return duration_periods / frequency


def calculate_modified_duration(
    macaulay_duration: float,
    ytm: float,
    frequency: int = 2,
) -> float:
    """
    Modified duration measures approximate
    percentage price sensitivity to yield changes.
    """

    denominator = (
        1 + ytm / frequency
    )

    if denominator <= 0:
        raise ValueError("Invalid YTM.")

    return macaulay_duration / denominator


def calculate_price_sensitivity(
    modified_duration: float,
    yield_change: float,
) -> float:
    """
    Approximate percentage price change from
    a yield change.

    Example:
    yield_change = 0.01 means +100 basis points.
    """

    return -modified_duration * yield_change


def calculate_accrued_interest(
    face_value: float,
    coupon_rate: float,
    days_since_coupon: int,
    coupon_period_days: int = 182,
) -> float:
    """
    Simplified accrued-interest calculation.
    """

    if days_since_coupon < 0:
        raise ValueError(
            "Days since coupon cannot be negative."
        )

    if coupon_period_days <= 0:
        raise ValueError(
            "Coupon period must be positive."
        )

    annual_coupon = (
        face_value * coupon_rate
    )

    return (
        annual_coupon
        * days_since_coupon
        / coupon_period_days
    )


def classify_credit_risk(
    credit_rating: str | None,
) -> str:
    """
    Broad credit-risk classification.

    This is an analytical classification,
    not an official rating.
    """

    if not credit_rating:
        return "unknown"

    rating = credit_rating.upper().strip()

    if rating in {
        "AAA",
        "Aaa",
    }:
        return "very_low"

    if rating in {
        "AA+",
        "AA",
        "AA-",
        "Aa1",
        "Aa2",
        "Aa3",
    }:
        return "low"

    if rating in {
        "A+",
        "A",
        "A-",
        "A1",
        "A2",
        "A3",
    }:
        return "moderate"

    if rating in {
        "BBB+",
        "BBB",
        "BBB-",
        "Baa1",
        "Baa2",
        "Baa3",
    }:
        return "medium_high"

    return "high"


def classify_interest_rate_risk(
    modified_duration: float,
) -> str:
    """
    Heuristic interest-rate-risk classification.
    """

    if modified_duration < 2:
        return "low"

    if modified_duration < 5:
        return "moderate"

    if modified_duration < 8:
        return "high"

    return "very_high"


def analyze_bond_intelligence(
    price: float,
    coupon_rate: float,
    face_value: float,
    years_to_maturity: float,
    credit_rating: str | None = None,
    frequency: int = 2,
) -> dict:
    """
    Generate a complete bond intelligence report.
    """

    logger.info(
        "Starting bond intelligence analysis."
    )

    current_yield = calculate_current_yield(
        price=price,
        coupon_rate=coupon_rate,
        face_value=face_value,
    )

    ytm = calculate_ytm(
        price=price,
        coupon_rate=coupon_rate,
        face_value=face_value,
        years_to_maturity=years_to_maturity,
        frequency=frequency,
    )

    macaulay_duration = calculate_macaulay_duration(
        price=price,
        coupon_rate=coupon_rate,
        face_value=face_value,
        years_to_maturity=years_to_maturity,
        ytm=ytm,
        frequency=frequency,
    )

    modified_duration = calculate_modified_duration(
        macaulay_duration=macaulay_duration,
        ytm=ytm,
        frequency=frequency,
    )

    convexity = calculate_convexity(
    price=price,
    coupon_rate=coupon_rate,
    face_value=face_value,
    years_to_maturity=years_to_maturity,
    ytm=ytm,
    frequency=frequency
    )

    price_sensitivity_100bp = calculate_price_sensitivity(
        modified_duration,
        0.01,
    )

    credit_risk = classify_credit_risk(
        credit_rating
    )

    interest_rate_risk = classify_interest_rate_risk(
        modified_duration
    )

    result = {
        "valuation": {
            "price": price,
            "face_value": face_value,
            "coupon_rate": coupon_rate,
            "current_yield": current_yield,
            "ytm": ytm,
        },
        "duration": {
            "macaulay_duration": macaulay_duration,
            "modified_duration": modified_duration,
            "convexity": convexity,
        },
        "interest_rate_risk": {
            "classification": interest_rate_risk,
            "estimated_price_change_for_100bp":
                price_sensitivity_100bp,
        },
        "credit_risk": {
            "rating": credit_rating,
            "classification": credit_risk,
        },
    }

    logger.info(
        "Bond intelligence analysis completed."
    )

    return result

def calculate_convexity(
    price: float,
    coupon_rate: float,
    face_value: float,
    years_to_maturity: float,
    ytm: float,
    frequency: int = 2,
) -> float:
    """
    Calculate approximate bond convexity.
    """

    periods = int(round(
        years_to_maturity * frequency
    ))

    coupon = (
        face_value
        * coupon_rate
        / frequency
    )

    periodic_yield = ytm / frequency

    if 1 + periodic_yield <= 0:
        raise ValueError("Invalid YTM.")

    weighted_cash_flows = 0.0
    present_value = 0.0

    for period in range(1, periods + 1):

        cash_flow = coupon

        if period == periods:
            cash_flow += face_value

        discounted = (
            cash_flow
            / (1 + periodic_yield) ** period
        )

        weighted_cash_flows += (
            period
            * (period + 1)
            * discounted
        )

        present_value += discounted

    if present_value <= 0:
        raise ValueError(
            "Unable to calculate convexity."
        )

    return (
        weighted_cash_flows
        / (
            present_value
            * frequency ** 2
        )
    )