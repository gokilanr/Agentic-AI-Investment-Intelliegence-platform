import pandas as pd
import numpy as np

from utils.logger import get_logger

logger = get_logger(__name__)


def calculate_growth_metrics(
    financials: pd.DataFrame
) -> dict:
    """
    Calculate company growth metrics.
    """

    logger.info("Calculating growth metrics.")

    revenue_growth = np.nan
    earnings_growth = np.nan

    if "Revenue" in financials.columns:
        revenue = financials["Revenue"].dropna()

        if len(revenue) >= 2:
            revenue_growth = (
                revenue.iloc[-1] / revenue.iloc[-2]
            ) - 1

    if "Net_Income" in financials.columns:
        earnings = financials["Net_Income"].dropna()

        if len(earnings) >= 2:
            previous = earnings.iloc[-2]
            current = earnings.iloc[-1]

            if previous != 0:
                earnings_growth = (
                    current / previous
                ) - 1

    return {
        "revenue_growth": revenue_growth,
        "earnings_growth": earnings_growth,
    }

def calculate_profitability_metrics(
    financials: pd.DataFrame
) -> dict:
    """
    Calculate company profitability metrics.
    """

    logger.info("Calculating profitability metrics.")

    latest = financials.iloc[-1]

    revenue = latest.get(
        "Revenue",
        np.nan
    )

    net_income = latest.get(
        "Net_Income",
        np.nan
    )

    total_assets = latest.get(
        "Total_Assets",
        np.nan
    )

    total_equity = latest.get(
        "Total_Equity",
        np.nan
    )

    net_margin = np.nan
    roa = np.nan
    roe = np.nan

    if revenue != 0 and not pd.isna(revenue):
        net_margin = net_income / revenue

    if (
        total_assets != 0
        and not pd.isna(total_assets)
    ):
        roa = net_income / total_assets

    if (
        total_equity != 0
        and not pd.isna(total_equity)
    ):
        roe = net_income / total_equity

    return {
        "net_margin": net_margin,
        "roa": roa,
        "roe": roe,
    }

def calculate_financial_health(
    financials: pd.DataFrame
) -> dict:
    """
    Calculate basic financial health metrics.
    """

    logger.info("Calculating financial health metrics.")

    latest = financials.iloc[-1]

    total_debt = latest.get(
        "Total_Debt",
        np.nan
    )

    total_equity = latest.get(
        "Total_Equity",
        np.nan
    )

    current_assets = latest.get(
        "Current_Assets",
        np.nan
    )

    current_liabilities = latest.get(
        "Current_Liabilities",
        np.nan
    )

    debt_to_equity = np.nan
    current_ratio = np.nan

    if (
        total_equity != 0
        and not pd.isna(total_equity)
    ):
        debt_to_equity = (
            total_debt / total_equity
        )

    if (
        current_liabilities != 0
        and not pd.isna(current_liabilities)
    ):
        current_ratio = (
            current_assets / current_liabilities
        )

    return {
        "debt_to_equity": debt_to_equity,
        "current_ratio": current_ratio,
    }

def calculate_cash_flow_metrics(
    financials: pd.DataFrame
) -> dict:
    """
    Calculate basic cash flow metrics.
    """

    logger.info("Calculating cash flow metrics.")

    latest = financials.iloc[-1]

    operating_cash_flow = latest.get(
        "Operating_Cash_Flow",
        np.nan
    )

    capital_expenditure = latest.get(
        "Capital_Expenditure",
        np.nan
    )

    free_cash_flow = np.nan

    if (
        not pd.isna(operating_cash_flow)
        and not pd.isna(capital_expenditure)
    ):
        free_cash_flow = (
            operating_cash_flow
            - abs(capital_expenditure)
        )

    return {
        "operating_cash_flow": operating_cash_flow,
        "capital_expenditure": capital_expenditure,
        "free_cash_flow": free_cash_flow,
    }


def analyze_fundamentals(
    financials: pd.DataFrame,
    ticker: str
) -> dict:
    """
    Generate a complete fundamental analysis.
    """

    logger.info(
        f"Starting fundamental analysis for {ticker}."
    )

    growth = calculate_growth_metrics(
        financials
    )

    profitability = calculate_profitability_metrics(
        financials
    )

    financial_health = calculate_financial_health(
        financials
    )

    cash_flow = calculate_cash_flow_metrics(
        financials
    )

    analysis = {
        "ticker": ticker,
        "growth": growth,
        "profitability": profitability,
        "financial_health": financial_health,
        "cash_flow": cash_flow,
    }

    logger.info(
        f"Fundamental analysis completed for {ticker}."
    )

    return analysis
