# from langchain_community.llms import Ollama


# def get_llm():
#     """
#     Returns the local Ollama LLM.
#     """
#     return Ollama(model="llama3.1:8b")

from langchain_ollama import OllamaLLM, ChatOllama


def get_llm():
    """LLM used by the RAG chain."""
    return OllamaLLM(
        model="llama3.1:8b"
    )


def get_chat_llm():
    """Chat model used by LangChain Agents."""
    return ChatOllama(
        model="llama3.1:8b",
        temperature=0
    )