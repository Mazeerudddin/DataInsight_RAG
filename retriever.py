from langchain_huggingface import (
    HuggingFaceEmbeddings,
)

from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

PERSIST_DIR = "./vector_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Single shared Chroma handle. Both retrieval (retrieve) and live
# ingestion (ingestion.ingest_document -> get_db().add_documents) use
# THIS instance, so freshly uploaded files are immediately searchable
# without restarting the app.
_db = None


def get_db():
    """Return the shared, persistent Chroma store (created lazily)."""
    global _db
    if _db is None:
        _db = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embeddings,
        )
    return _db


def retrieve(question, k=5):
    return get_db().similarity_search(question, k=k)


if __name__ == "__main__":

    while True:

        question = input("\nQuestion: ")

        if question.lower() == "exit":
            break

        docs = retrieve(question)

        for i, doc in enumerate(docs, start=1):
            print(f"\n===== CHUNK {i} =====")
            print("\nMETADATA:")
            print(doc.metadata)
            print("\nCONTENT:")
            print(doc.page_content[:500])
