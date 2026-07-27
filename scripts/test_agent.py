from agents.langchain_agent import agent_executor

while True:
    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    response = agent_executor.invoke(
        {
            "input": question
        }
    )

    print("\nAnswer:\n")
    print(response["output"])