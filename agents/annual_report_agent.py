from rag.rag_engine import RAGEngine


class AnnualReportAgent:

    def __init__(self):
        self.rag = RAGEngine()

    def run(self, question: str) -> dict:
        print(">>> Annual report Agent")
        response = self.rag.ask(question)

        return {
            "agent": "Annual Report",
            "answer": response["result"],
            "sources": response.get("source_documents", [])
        }