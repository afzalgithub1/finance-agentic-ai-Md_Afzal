from rag.retriever import get_vector_db

db = get_vector_db()

print("=" * 50)
print("WITHOUT FILTER")
print("=" * 50)

docs = db.similarity_search(
    "SBI",
    k=4
)

for doc in docs:
    print(doc.metadata)

print("\n")

print("=" * 50)
print("WITH FILTER")
print("=" * 50)

docs = db.similarity_search(
    "SBI",
    k=4,
    filter={"company": "SBIN"}
)

for doc in docs:
    print(doc.metadata)