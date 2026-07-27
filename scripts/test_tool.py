from agents.tools import fundamentals_tool, annual_report_tool

print(fundamentals_tool.invoke("ROE of SBI"))

print("=" * 50)

print(annual_report_tool.invoke("Summarize Infosys"))