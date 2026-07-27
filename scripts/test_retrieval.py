import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# ==============================================================================
# 1. PATH CONFIGURATION
# Dynamically locate the project root and point to the ChromaDB directory
# ==============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DB_DIR = os.path.join(PROJECT_ROOT, "vector_db", "chroma_annual_reports")

def test_vector_db_retrieval():
    """
    Connects to the persisted Chroma vector database and performs a top-K
    similarity search to verify document indexing and metadata retrieval.
    """
    print("Loading local vector database...")
    
    # Initialize the same embedding model used during PDF ingestion
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Re-open the saved Chroma vector database from disk
    vector_db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )

    # Define a test financial query
    test_query = "What are the major revenue drivers for Reliance or TCS?"
    print(f"\n[QUERY]: '{test_query}'\n")

    # Search the vector database
        # Search the vector database
    results = vector_db.similarity_search(test_query, k=5)

    print("=" * 80)
    print(f"Retrieved {len(results)} documents")
    print("=" * 80)

    for i, doc in enumerate(results, 1):
        print(f"\nResult #{i}")
        print("-" * 60)
        print("Source:", doc.metadata.get("source", "Unknown"))
        print("Page:", doc.metadata.get("page", "Unknown"))
        print("\nContent:")
        print(doc.page_content[:500])


if __name__ == "__main__":
    test_vector_db_retrieval()
