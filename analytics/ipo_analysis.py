from utils.logger import get_logger

from analytics.ipo_profile import (
    create_ipo_profile
)

from analytics.ipo_intelligence import (
    analyze_ipo_intelligence
)


logger = get_logger(__name__)


def build_ipo_analysis(
    ipo_id: str,
    company_name: str,
    sector: str,
    exchange: str,
    issue_price: float,
    issue_size: float,
    lot_size: int,
    revenue_growth: float,
    profit_growth: float,
    net_margin: float,
    debt_to_equity: float,
    pe_ratio: float,
    subscription_ratio: float,
    listing_price: float | None = None,
    fresh_issue_percentage: float | None = None,
    ofs_percentage: float | None = None,
    promoter_holding: float | None = None,
) -> dict:
    """
    Build complete IPO analysis.
    """

    logger.info(
        f"Building IPO analysis for {ipo_id}."
    )

    profile = create_ipo_profile(
        ipo_id=ipo_id,
        company_name=company_name,
        sector=sector,
        exchange=exchange,
        issue_price=issue_price,
        issue_size=issue_size,
        lot_size=lot_size,
        fresh_issue_percentage=
            fresh_issue_percentage,
        ofs_percentage=ofs_percentage,
        promoter_holding=promoter_holding,
    )

    intelligence = analyze_ipo_intelligence(
        company_name=company_name,
        issue_price=issue_price,
        issue_size=issue_size,
        revenue_growth=revenue_growth,
        profit_growth=profit_growth,
        net_margin=net_margin,
        debt_to_equity=debt_to_equity,
        pe_ratio=pe_ratio,
        subscription_ratio=subscription_ratio,
        listing_price=listing_price,
        fresh_issue_percentage=
            fresh_issue_percentage,
        promoter_holding=promoter_holding,
    )

    return {
        "profile": profile,
        "intelligence": intelligence,
    }