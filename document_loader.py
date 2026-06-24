import os

from langchain_community.document_loaders import (
    PyMuPDFLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader,
)


def load_file(path):
    """
    Load a single document file into a list of LangChain Documents.

    Returns [] for unsupported types or on failure, and always tags each
    document with its source filename so citations work later.
    """
    file = os.path.basename(path)

    try:
        if file.endswith(".pdf"):
            loader = PyMuPDFLoader(path)

        elif file.endswith(".docx"):
            loader = Docx2txtLoader(path)

        elif file.endswith(".pptx"):
            loader = UnstructuredPowerPointLoader(path)

        else:
            return []

        docs = loader.load()

        for doc in docs:
            doc.metadata["source_file"] = file

        print(f"Loaded: {file}")
        return docs

    except Exception as e:
        print(f"Failed: {file}")
        print(e)
        return []


def load_documents(folder="knowledge_base"):
    """Load every supported document in a folder."""
    documents = []

    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        return documents

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        documents.extend(load_file(path))

    return documents


if __name__ == "__main__":

    docs = load_documents()

    print(f"\nDocuments Loaded: {len(docs)}")

    for doc in docs[:5]:
        print("\nSOURCE:")
        print(doc.metadata.get("source_file"))
        print("\nCONTENT:")
        print(doc.page_content[:300])
