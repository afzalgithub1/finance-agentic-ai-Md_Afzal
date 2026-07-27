import time

from agents.langchain_agent import agent_executor
from context.context_manager import ConversationContext


def ask_agent(question: str):

    ConversationContext.initialize()

    rewritten_question = ConversationContext.rewrite_question(question)

    print("=" * 60)
    print("Original Question :", question)
    print("Rewritten Question:", rewritten_question)

    start = time.perf_counter()

    print("\n========== INPUT TO AGENT ==========")
    print(rewritten_question)
    print("===================================\n")

    response = agent_executor.invoke(
        {
            "input": rewritten_question
        }
    )

    total_time = time.perf_counter() - start

    print("\nResponse Keys:")
    print(response.keys())

    # print("\nIntermediate Steps:")
    # print(response.get("intermediate_steps"))

    print("\n========== INTERMEDIATE STEPS ==========")

    steps = response.get("intermediate_steps", [])

    for i, (action, observation) in enumerate(steps, start=1):
        print(f"\nStep {i}")
        print("Tool :", action.tool)
        print("Tool Input :", action.tool_input)
        print("Observation :", observation)

    print("=======================================\n")

    print(f"\nTotal Time: {total_time:.2f} sec")
    print("=" * 60)

    answer = response["output"]

    tool_output = None
    agent_used = "LLM"

    steps = response.get("intermediate_steps", [])

    if steps:

        action, observation = steps[-1]

        tool_output = observation
        agent_used = action.tool

    ConversationContext.update_context(
        rewritten_question,
        agent_used
    )

    return (
        tool_output,
        answer,
        agent_used,
        total_time,
    )