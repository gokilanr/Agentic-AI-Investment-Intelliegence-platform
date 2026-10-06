from utils.logger import get_logger

logger = get_logger(__name__)


def create_bond_profile(
    bond_id: str,
    issuer: str,
    bond_type: str,
    coupon_rate: float,
    maturity_years: float,
    face_value: float = 100.0,
    credit_rating: str | None = None,
) -> dict:
    """
    Create a standardized bond profile.
    """

    if not bond_id:
        raise ValueError(
            "Bond ID cannot be empty."
        )

    if not issuer:
        raise ValueError(
            "Issuer cannot be empty."
        )

    if coupon_rate < 0:
        raise ValueError(
            "Coupon rate cannot be negative."
        )

    if maturity_years <= 0:
        raise ValueError(
            "Maturity must be greater than zero."
        )

    if face_value <= 0:
        raise ValueError(
            "Face value must be greater than zero."
        )

    profile = {
        "bond_id": bond_id,
        "issuer": issuer,
        "bond_type": bond_type,
        "coupon_rate": coupon_rate,
        "maturity_years": maturity_years,
        "face_value": face_value,
        "credit_rating": credit_rating,
    }

    logger.info(
        f"Bond profile created for {bond_id}."
    )

    return profile