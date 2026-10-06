from utils.logger import get_logger


logger = get_logger(__name__)


def create_ipo_profile(
    ipo_id: str,
    company_name: str,
    sector: str,
    exchange: str,
    issue_price: float,
    issue_size: float,
    lot_size: int,
    fresh_issue_percentage: float | None = None,
    ofs_percentage: float | None = None,
    promoter_holding: float | None = None,
) -> dict:
    """
    Create standardized IPO metadata.
    """

    if not ipo_id:
        raise ValueError(
            "IPO ID cannot be empty."
        )

    if not company_name:
        raise ValueError(
            "Company name cannot be empty."
        )

    if issue_price <= 0:
        raise ValueError(
            "Issue price must be greater than zero."
        )

    if issue_size <= 0:
        raise ValueError(
            "Issue size must be greater than zero."
        )

    if lot_size <= 0:
        raise ValueError(
            "Lot size must be greater than zero."
        )

    profile = {
        "ipo_id": ipo_id,
        "company_name": company_name,
        "sector": sector,
        "exchange": exchange,
        "issue_price": issue_price,
        "issue_size": issue_size,
        "lot_size": lot_size,
        "fresh_issue_percentage":
            fresh_issue_percentage,
        "ofs_percentage":
            ofs_percentage,
        "promoter_holding":
            promoter_holding,
    }

    logger.info(
        f"IPO profile created for {ipo_id}."
    )

    return profile