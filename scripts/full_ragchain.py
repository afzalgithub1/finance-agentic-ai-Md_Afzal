import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# ==============================================================================
# 1. PATH CONFIGURATION
# Dynamically locate the project root and point to the ChromaDB directory
# ==============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DB_DIR = os.path.join(PROJECT_ROOT, "vector_db", "chroma_annual_reports")

def build_rag_agent(model_name="llama3.1:8b"):
    """
    Constructs a RetrievalQA chain combining local ChromaDB vector retrieval
    with a local Ollama LLM.
    
    Args:
        model_name (str): Ollama LLM model to use for generating answers.
        
    Returns:
        RetrievalQA: Configured LangChain RetrievalQA instance.
    """
    print("Initializing Embeddings and Vector Database connection...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Load ChromaDB from local disk
    vector_db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )
    
    # Convert vector database into a LangChain Retriever (fetches top 4 relevant chunks)
    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
    
    print(f"Initializing local LLM ('{model_name}')...")
    # Initialize the local LLM via Ollama (e.g., llama3, mistral, qwen2.5)
    llm = Ollama(model=model_name)

    # ==============================================================================
    # 2. RETRIEVAL QA CHAIN SETUP
    # - 'chain_type="stuff"' injects retrieved chunks directly into the prompt context
    # - 'return_source_documents=True' allows us to inspect metadata/sources used
    # ==============================================================================
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    
    return qa_chain

def run_agent_query(query_text):
    """
    Executes a user query through the RAG chain and prints the answer + citations.
    """
    # Create the agent
    agent = build_rag_agent(model_name="llama3.1:8b")
    
    print(f"\n[USER QUESTION]: {query_text}\n")
    print("Generating response from retrieved context...\n")
    
    # Pass the query to the RAG chain
    response = agent.invoke({"query": query_text})
    
    # Display LLM Output
    print("=" * 20 + " AGENT ANSWER " + "=" * 20)
    print(response["result"])
    print("=" * 54)
    
    # Display Source Documents used for answer synthesis
    print("\n" + "=" * 18 + " SOURCES REFERENCED " + "=" * 18)
    for idx, doc in enumerate(response["source_documents"], 1):
        ticker = doc.metadata.get("company", "N/A")
        source = doc.metadata.get("source", "N/A")
        print(f"[{idx}] Ticker: {ticker} | File: {source}")
    print("=" * 56)

if __name__ == "__main__":
    user_question = input("Ask a financial question: ")
    run_agent_query(user_question)
