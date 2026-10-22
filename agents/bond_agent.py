
from analytics.bond_analysis import build_bond_analysis
from utils.logger import get_logger

logger = get_logger(__name__)


def run_bond_agent(
    bond_id: str,
    issuer: str,
    bond_type: str,
    price: float,
    coupon_rate: float,
    maturity_years: float,
    face_value: float = 100.0,
    credit_rating: str | None = None,
    frequency: int = 2,
) -> dict:
    """Build a structured bond profile and intelligence report."""

    if not bond_id or not bond_id.strip():
        raise ValueError("Bond ID cannot be empty.")

    if not issuer or not issuer.strip():
        raise ValueError("Issuer cannot be empty.")

    if not bond_type or not bond_type.strip():
        raise ValueError("Bond type cannot be empty.")

    if price <= 0:
        raise ValueError("Bond price must be greater than zero.")

    if face_value <= 0:
        raise ValueError("Face value must be greater than zero.")

    if maturity_years <= 0:
        raise ValueError("Maturity must be greater than zero.")

    if not 0 <= coupon_rate <= 1:
        raise ValueError(
            "Coupon rate must be expressed as a decimal between 0 and 1."
        )

    if frequency < 1:
        raise ValueError("Frequency must be at least 1.")

    logger.info("Running bond agent for %s", bond_id)

    analysis = build_bond_analysis(
        bond_id=bond_id.strip(),
        issuer=issuer.strip(),
        bond_type=bond_type.strip(),
        price=price,
        coupon_rate=coupon_rate,
        maturity_years=maturity_years,
        face_value=face_value,
        credit_rating=credit_rating,
        frequency=frequency,
    )

    return {
        "agent": "bond_agent",
        "status": "success",
        "bond_id": bond_id.strip(),
        "analysis": analysis,
    }
