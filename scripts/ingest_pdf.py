import os
import re
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Dynamically locate project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DATA_DIR = os.path.join(PROJECT_ROOT, "data", "annual report")
DB_DIR = os.path.join(PROJECT_ROOT, "vector_db", "chroma_annual_reports")

def get_ticker_from_filename(filename):
    match = re.search(r"AR_\d+_([A-Z0-9&]+)_", filename)
    return match.group(1) if match else "UNKNOWN"

def run_ingestion():
    if not os.path.exists(DATA_DIR):
        print(f"Error: Folder '{DATA_DIR}' not found.")
        return

    pdf_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDF files in '{DATA_DIR}'.\n")

    all_docs = []
    for idx, pdf in enumerate(pdf_files, 1):
        file_path = os.path.join(DATA_DIR, pdf)
        ticker = get_ticker_from_filename(pdf)
        print(f"[{idx}/{len(pdf_files)}] Reading: {pdf} (Ticker: {ticker})")

        loader = PyMuPDFLoader(file_path)
        pages = loader.load()

        for page in pages:
            page.metadata["company"] = ticker
            page.metadata["source"] = pdf

        all_docs.extend(pages)

    print(f"\nSuccessfully read {len(all_docs)} pages.")
    print("Splitting pages into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(all_docs)
    total_chunks = len(chunks)
    print(f"Created {total_chunks} text chunks.")

    print("\nConnecting to local Ollama ('nomic-embed-text')...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # BATCHING LOGIC
    BATCH_SIZE = 500
    total_batches = (total_chunks + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"Total batches to process: {total_batches}")
    print(f"Saving vector database to '{DB_DIR}' in batches of {BATCH_SIZE}...\n")

    # Initialize Chroma database with the first batch
    first_batch = chunks[:BATCH_SIZE]
    vector_db = Chroma.from_documents(
        documents=first_batch,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print(f"Processed batch 1/{total_batches} ({len(first_batch)}/{total_chunks} chunks)")

    # Add remaining chunks in small batches
    for i in range(BATCH_SIZE, total_chunks, BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        vector_db.add_documents(batch)
        batch_num = (i // BATCH_SIZE) + 1
        processed_count = min(i + len(batch), total_chunks)
        print(f"Processed batch {batch_num}/{total_batches} ({processed_count}/{total_chunks} chunks)")

    print("\nDone! Vector database created safely and stored locally.")

if __name__ == "__main__":
    run_ingestion()