from langchain_core.prompts import PromptTemplate

from rag.llm import get_llm
from rag.prompts import FINANCE_PROMPT
from rag.retriever import get_retriever
from rag.company_detector import detect_company


class RAGEngine:

    def __init__(self):
        self.llm = get_llm()

    def ask(self, question):

        company = detect_company(question)

        retriever = get_retriever(company)

        docs = retriever.invoke(question)

        # print("\n" + "=" * 80)
        # print(f"Detected Company: {company}")
        # print(f"Retrieved {len(docs)} documents")
        # print("=" * 80)

        # for i, doc in enumerate(docs, 1):
        #     print(f"\nDocument {i}")
        #     print("Metadata:", doc.metadata)
        #     print("\nContent Preview:")
        #     print(doc.page_content[:1000])   # Print first 1000 characters
        #     print("-" * 80)

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        prompt = FINANCE_PROMPT.format(
            context=context,
            question=question
        )
        answer = self.llm.invoke(prompt)

        return {
            "result": answer,
            "source_documents": docs
        }