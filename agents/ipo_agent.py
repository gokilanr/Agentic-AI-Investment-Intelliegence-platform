
from analytics.ipo_analysis import build_ipo_analysis
from utils.logger import get_logger

logger = get_logger(__name__)


def run_ipo_agent(
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
    """Validate IPO inputs and return a complete IPO analysis."""

    required_strings = {
        "IPO ID": ipo_id,
        "Company name": company_name,
        "Sector": sector,
        "Exchange": exchange,
    }

    for field, value in required_strings.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} cannot be empty.")

    if issue_price <= 0:
        raise ValueError("Issue price must be greater than zero.")

    if issue_size <= 0:
        raise ValueError("Issue size must be greater than zero.")

    if not isinstance(lot_size, int) or isinstance(lot_size, bool) or lot_size < 1:
        raise ValueError("Lot size must be a positive integer.")

    if subscription_ratio < 0:
        raise ValueError("Subscription ratio cannot be negative.")

    if listing_price is not None and listing_price <= 0:
        raise ValueError("Listing price must be greater than zero.")

    percentages = {
        "Fresh issue percentage": fresh_issue_percentage,
        "OFS percentage": ofs_percentage,
        "Promoter holding": promoter_holding,
    }

    for field, value in percentages.items():
        if value is not None and not 0 <= value <= 100:
            raise ValueError(f"{field} must be between 0 and 100.")

    ipo_id = ipo_id.strip()
    company_name = company_name.strip()
    sector = sector.strip()
    exchange = exchange.strip()

    logger.info("Running IPO agent for %s.", ipo_id)

    analysis = build_ipo_analysis(
        ipo_id=ipo_id,
        company_name=company_name,
        sector=sector,
        exchange=exchange,
        issue_price=issue_price,
        issue_size=issue_size,
        lot_size=lot_size,
        revenue_growth=revenue_growth,
        profit_growth=profit_growth,
        net_margin=net_margin,
        debt_to_equity=debt_to_equity,
        pe_ratio=pe_ratio,
        subscription_ratio=subscription_ratio,
        listing_price=listing_price,
        fresh_issue_percentage=fresh_issue_percentage,
        ofs_percentage=ofs_percentage,
        promoter_holding=promoter_holding,
    )

    return {
        "agent": "ipo_agent",
        "status": "success",
        "ipo_id": ipo_id,
        "company_name": company_name,
        "analysis": analysis,
    }
