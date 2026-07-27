import os

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_DIR = os.path.join(
    PROJECT_ROOT,
    "vector_db",
    "chroma_annual_reports"
)


def get_vector_db():

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )


# def get_retriever():

#     vector_db = get_vector_db()

#     return vector_db.as_retriever(
#         search_type="similarity",
#         search_kwargs={"k":4}
#     )

def get_retriever(company=None):
    vector_db = get_vector_db()

    search_kwargs = {"k": 4}

    if company:
        search_kwargs["filter"] = {
            "company": company
        }

    search_kwargs = {
        "k": 10,
        "fetch_k": 40
    }

    if company:
        search_kwargs["filter"] = {"company": company}

    return vector_db.as_retriever(
        search_type="mmr",
        search_kwargs=search_kwargs
    )