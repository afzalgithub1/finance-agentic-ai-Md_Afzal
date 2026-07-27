from agents.langchain_agent import agent_executor


def main():
    print("=" * 70)
    print("Financial Assistant (LangChain Agent)")
    print("Type 'exit' to quit")
    print("=" * 70)

    while True:
        question = input("\nAsk: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        try:
            response = agent_executor.invoke(
                {
                     "input": question
                }
            )

            print("\nAnswer:\n")
            print(response["output"])

            # Display which tool/agent was used
            if response.get("intermediate_steps"):

                tool_name = response["intermediate_steps"][0][0].tool

                tool_map = {
                    "fundamentals_tool": "Fundamentals Agent",
                    "annual_report_tool": "Annual Report Agent",
                    "prediction_tool": "Prediction Agent",
                    "comparison_tool": "Comparison Agent",
                }

                print("\nAgent Used:")
                print(tool_map.get(tool_name, tool_name))

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()