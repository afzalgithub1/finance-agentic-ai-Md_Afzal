from langchain.tools import tool
from pydantic import BaseModel, Field
from agents.fundamentals_agent import FundamentalsAgent
from agents.annual_report_agent import AnnualReportAgent
from agents.prediction_agent import prediction_tool
from agents.comparison_agent import comparison_tool


fundamentals_agent = FundamentalsAgent()
annual_report_agent = AnnualReportAgent()

class FundamentalsInput(BaseModel):
    company_name: str = Field(
        description="Company name"
    )

    metric: str = Field(
        description="Financial metric to retrieve. Examples: ROE, ROCE, PE, EPS, Revenue, Sales, Market Cap, Book Value, Debt, Dividend Yield, Face Value, Current Price."
    )

class AnnualReportInput(BaseModel):
    company_name: str = Field(
        description="Company name"
    )

    query: str = Field(
        description="User question about the company such as company overview, annual report summary, CEO message, business overview, risks, strategy or sustainability."
    )

@tool(args_schema=FundamentalsInput)
def fundamentals_tool(
    company_name: str,
    metric: str,
) -> str:
    """
    Use ONLY for financial metrics.

    Examples:
    - ROE
    - ROCE
    - PE
    - EPS
    - Revenue
    - Sales
    - Market Cap
    - Book Value
    - Debt
    - Dividend Yield
    - Face Value
    - Current Price

    Do NOT use for:
    - Tell me about a company
    - Company overview
    - Explain a company
    """

    question = f"{metric} of {company_name}"

    response = fundamentals_agent.run(question)

    return response["answer"]


@tool(args_schema=AnnualReportInput)
def annual_report_tool(
    company_name: str,
    query: str,
) -> str:
    """
    Use this tool for general company information.

    Examples:
    - Tell me about TCS
    - Explain Infosys
    - Company overview
    - Annual report summary
    - CEO message
    - Risks
    - Strategy
    - Sustainability
    - Business overview
    """

    question = f"{query} of {company_name}"

    response = annual_report_agent.run(question)

    return response["answer"]