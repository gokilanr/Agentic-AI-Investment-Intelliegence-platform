
from agents.stock_agent import run_stock_agent
from agents.company_agent import run_company_agent
from agents.fund_agent import run_fund_agent
from agents.bond_agent import run_bond_agent
from agents.ipo_agent import run_ipo_agent
from utils.logger import get_logger

logger = get_logger(__name__)


def route_investment_request(
    investment_type: str,
    parameters: dict,
) -> dict:
    """
    Route an investment request to the appropriate specialized agent.

    Supported types:
        stock, company, fund, bond, ipo
    """

    if not isinstance(investment_type, str) or not investment_type.strip():
        raise ValueError("Investment type cannot be empty.")

    if not isinstance(parameters, dict):
        raise ValueError("Parameters must be provided as a dictionary.")

    investment_type = investment_type.strip().lower()

    agents = {
        "stock": run_stock_agent,
        "company": run_company_agent,
        "fund": run_fund_agent,
        "bond": run_bond_agent,
        "ipo": run_ipo_agent,
    }

    agent_function = agents.get(investment_type)

    if agent_function is None:
        supported_types = ", ".join(agents.keys())
        raise ValueError(
            f"Unsupported investment type '{investment_type}'. "
            f"Supported types: {supported_types}."
        )

    logger.info("Routing investment request to %s agent.", investment_type)

    try:
        result = agent_function(**parameters)

        return {
            "status": "success",
            "investment_type": investment_type,
            "result": result,
        }

    except Exception:
        logger.exception(
            "Investment request failed for type '%s'.",
            investment_type,
        )
        raise
