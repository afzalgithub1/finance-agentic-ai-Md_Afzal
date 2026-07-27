from langchain.tools import tool

from agents.fundamentals_agent import FundamentalsAgent
from rag.company_detector import detect_company

fundamentals = FundamentalsAgent()


@tool
def comparison_tool(company_1: str, company_2: str) -> str:
    """
    Compare two companies based on key fundamental metrics.
    """

    company_1 = detect_company(company_1) or company_1
    company_2 = detect_company(company_2) or company_2

    metrics = [
        "Current Price",
        "Market Cap",
        "Stock P/E",
        "ROE",
        "ROCE",
        "EPS",
        "Book Value",
        "Dividend Yield",
        "Face Value",
        "Debt",
    ]

    response = f"# Company Comparison\n\n"
    response += f"**{company_1} vs {company_2}**\n\n"

    response += f"| Metric | {company_1} | {company_2} |\n"
    response += "|--------|--------|--------|\n"

    for metric in metrics:

        value1 = fundamentals.get_metric(company_1, metric)
        value2 = fundamentals.get_metric(company_2, metric)

        response += f"| {metric} | {value1} | {value2} |\n"

    return response