from dotenv import load_dotenv

load_dotenv()
from document_loader import load_documents

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_chroma import Chroma


def build_vector_db():

    print(
        "\nLoading documents..."
    )

    documents = load_documents()

    print(
        f"Loaded {len(documents)} documents"
    )

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Created {len(chunks)} chunks"
    )

    embeddings = (
        HuggingFaceEmbeddings(
            model_name=
            "sentence-transformers/all-MiniLM-L6-v2"
        )
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=
        "./vector_db"
    )

    print(
        "\nVector DB created successfully"
    )


if __name__ == "__main__":

    build_vector_db()