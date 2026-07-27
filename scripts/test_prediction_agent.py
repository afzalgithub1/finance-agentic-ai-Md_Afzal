from agents.prediction_agent import prediction_tool

print(
    prediction_tool.invoke(
        {
            "company_name": "HDFC_BANK"
        }
    )
)

print()

print(
    prediction_tool.invoke(
        {
            "company_name": "RELIANCE"
        }
    )
)