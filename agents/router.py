from agents.annual_report_agent import AnnualReportAgent
from agents.fundamentals_agent import FundamentalsAgent


class Router:

    FUNDAMENTAL_KEYWORDS = [
        "pe",
        "p/e",
        "roe",
        "roce",
        "eps",
        "market cap",
        "book value",
        "dividend",
        "face value",
        "current price",
        "price to sales",
        "debt",
        "sales growth",
        "profit growth",
        "revenue",
        "sales",
        "operating profit",
        "expenses",
        "profit before tax",
        "cash flow"
    ]

    def __init__(self):
        self.annual_report_agent = AnnualReportAgent()
        self.fundamentals_agent = FundamentalsAgent()

    def route(self, question: str):

        question_lower = question.lower()

        for keyword in self.FUNDAMENTAL_KEYWORDS:
            if keyword in question_lower:
                return self.fundamentals_agent.run(question)

        return self.annual_report_agent.run(question)