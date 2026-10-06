from utils.logger import get_logger

from analytics.bond_profile import (
    create_bond_profile
)

from analytics.bond_intelligence import (
    analyze_bond_intelligence
)


logger = get_logger(__name__)


def build_bond_analysis(
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
    """
    Build complete bond analysis.
    """

    logger.info(
        f"Building bond analysis for {bond_id}."
    )

    profile = create_bond_profile(
        bond_id=bond_id,
        issuer=issuer,
        bond_type=bond_type,
        coupon_rate=coupon_rate,
        maturity_years=maturity_years,
        face_value=face_value,
        credit_rating=credit_rating,
    )

    intelligence = analyze_bond_intelligence(
        price=price,
        coupon_rate=coupon_rate,
        face_value=face_value,
        years_to_maturity=maturity_years,
        credit_rating=credit_rating,
        frequency=frequency,
    )

    return {
        "profile": profile,
        "intelligence": intelligence,
    }