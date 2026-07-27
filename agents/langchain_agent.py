from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

from agents.tools import (
    fundamentals_tool,
    annual_report_tool,
    prediction_tool,
    comparison_tool,
)

from rag.llm import get_chat_llm


llm = get_chat_llm()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a financial assistant.

Choose the correct tool:

- fundamentals_tool:
  PE, ROE, ROCE, EPS, Revenue, Sales, Market Cap,
  Book Value, Debt, Cash Flow, Dividend Yield,
  Face Value, Current Price.

- annual_report_tool:
  Use this tool for general company information.

  Examples:
  - Tell me about TCS
  - Explain Infosys
  - Company overview
  - Summarize annual report
  - CEO message
  - Business overview
  - Strategy
  - Risks
  - Sustainability
  - Management discussion

- prediction_tool:
  Predict the next trading day's closing price for a stock.
  Use this whenever the user asks for:
  - prediction
  - forecast
  - expected price
  - next closing price
  - tomorrow's price

- comparison_tool:
  Use this tool when the user asks to:
  - compare two companies
  - compare two stocks
  - compare fundamentals
  - compare financial metrics
  - which company is better

Always choose the most appropriate tool.

IMPORTANT:

Always choose the most appropriate tool.

If a tool returns:

- Metric not supported.
- Company data not available.
- Could not detect company.

Then choose another tool ONLY IF another tool can logically answer the user's question.

If the user's question is about:
- company overview
- business overview
- annual report summary
- CEO message
- management discussion
- strategy
- risks
- sustainability

DO NOT switch to fundamentals_tool.

If no tool can answer the question, tell the user that the requested information could not be found.

Only finish after successfully using the correct tool.

When a tool returns structured financial information
(such as comparison, prediction or fundamentals),

return the COMPLETE tool output exactly as returned.

Then add:

## AI Analysis

Provide a concise explanation in 4–8 sentences.

Never shorten or rewrite the tool output.
"""
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

tools = [
    fundamentals_tool,
    annual_report_tool,
    prediction_tool,
    comparison_tool,
]

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True,
)
