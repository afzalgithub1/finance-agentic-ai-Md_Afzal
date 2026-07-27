# from rag.rag_engine import RAGEngine


# engine = RAGEngine()


# while True:

#     question = input("\nAsk a financial question (or type 'exit'): ")

#     if question.lower() == "exit":
#         break

#     response = engine.ask(question)

#     print("\n")
#     print(response["result"])

from agents.router import Router

router = Router()

while True:

    question = input("\nAsk a financial question (or type 'exit'): ")

    if question.lower() == "exit":
        break

    response = router.route(question)

    print("\n")
    print(response["answer"])