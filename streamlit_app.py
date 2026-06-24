import os

import streamlit as st

from app import app
from ingestion import (
    save_uploaded_file,
    ingest_path,
    KNOWLEDGE_BASE,
)


st.set_page_config(
    page_title="RAG Copilot",
    layout="wide",
)

st.title("Multi-Agent RAG Copilot")

st.markdown(
    """
Ask questions about:

- PDFs
- CSVs
- Research Reports
- Structured Datasets

The system automatically chooses:

- RAG
- SQL
- Charts
- Hybrid Analysis
"""
)

os.makedirs(KNOWLEDGE_BASE, exist_ok=True)

# Track which uploads we've already ingested so Streamlit's per-interaction
# reruns don't re-embed / re-load the same file over and over.
if "ingested" not in st.session_state:
    st.session_state.ingested = set()


def handle_uploads(uploaded_files):
    """Save and ingest any files we haven't processed yet."""
    if not uploaded_files:
        return

    for uf in uploaded_files:
        # name + size is a cheap, reliable dedup key across reruns.
        key = (uf.name, uf.size)
        if key in st.session_state.ingested:
            continue

        try:
            path = save_uploaded_file(uf)
            with st.spinner(f"Indexing {uf.name}..."):
                result = ingest_path(path)

            if result["kind"] == "document":
                st.success(
                    f"Added to vector DB: {uf.name} "
                    f"({result['chunks']} chunks)"
                )
            elif result["kind"] == "dataset":
                st.success(
                    f"Added to SQLite: {uf.name} "
                    f"-> table '{result['table']}' "
                    f"({result['rows']} rows)"
                )
            else:
                st.warning(f"Skipped (unsupported): {uf.name}")

            st.session_state.ingested.add(key)

        except Exception as e:
            st.error(f"Failed to ingest {uf.name}: {e}")



with st.sidebar:

    st.header("Knowledge Base")

    uploaded_docs = st.file_uploader(
        "Upload documents (PDF / DOCX / PPTX)",
        type=["pdf", "docx", "pptx"],
        accept_multiple_files=True,
    )
    handle_uploads(uploaded_docs)

    uploaded_data = st.file_uploader(
        "Upload datasets (CSV / XLSX)",
        type=["csv", "xlsx"],
        accept_multiple_files=True,
    )
    handle_uploads(uploaded_data)

    st.divider()

    if st.session_state.ingested:
        st.caption("Ingested this session:")
        for name, _ in sorted(st.session_state.ingested):
            st.caption(f"- {name}")

    st.success("Vector Database Loaded")
    st.success("SQLite Database Loaded")
    st.info("Multi-Agent System Active")




if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])




question = st.chat_input("Ask a question...")

if question:

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    try:
        with st.spinner("Thinking..."):
            result = app(question)

        answer = result["answer"]
        chart_path = result["raw_results"].get("chart")

        with st.chat_message("assistant"):
            st.markdown(answer)

            if chart_path:
                st.image(
                    chart_path,
                    use_container_width=True,
                )

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")
