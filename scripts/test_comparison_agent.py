from agents.comparison_agent import comparison_tool

print(
    comparison_tool.invoke(
        {
            "company_1": "RELIANCE",
            "company_2": "TCS",
        }
    )
)