"""
Live ingestion for the Streamlit app.

This is the piece that was missing: when a file is uploaded, it must be
pushed into the SAME stores the agents read from at query time:

  - PDF / DOCX / PPTX  -> chunked, embedded, added to the Chroma vector DB
  - CSV / XLSX         -> loaded as a table into knowledge.db (SQLite)

Both the vector DB (via retriever.get_db) and SQLite (read live by
dataset_selector.get_table_catalog) pick the new content up immediately,
so no separate build_*.py run is needed.
"""

import os
import re
import sqlite3

import pandas as pd

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from document_loader import load_file
from retriever import get_db


KNOWLEDGE_BASE = "knowledge_base"
DB_NAME = "knowledge.db"

DOC_EXTS = (".pdf", ".docx", ".pptx")
DATA_EXTS = (".csv", ".xlsx")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)


def _safe_table_name(filename):
    """Turn a filename into a valid SQLite table name."""
    name = os.path.splitext(os.path.basename(filename))[0]
    # SQLite is fine with most names if quoted, but to_sql + our PRAGMA
    # usage is happiest with simple identifiers.
    name = re.sub(r"\W+", "_", name).strip("_")
    if not name:
        name = "dataset"
    if name[0].isdigit():
        name = "t_" + name
    return name


def ingest_document(path):
    """Add one PDF/DOCX/PPTX to the vector DB. Returns chunks added."""
    docs = load_file(path)

    if not docs:
        return 0

    chunks = splitter.split_documents(docs)

    if not chunks:
        return 0

    db = get_db()
    db.add_documents(chunks)
    # Chroma with a persist_directory writes through automatically in
    # langchain-chroma >= 0.1, so no manual .persist() call is needed.

    return len(chunks)


def ingest_dataset(path):
    """Load one CSV/XLSX into knowledge.db as a table. Returns (table, rows)."""
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    elif path.endswith(".xlsx"):
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported dataset type: {path}")

    table = _safe_table_name(path)

    conn = sqlite3.connect(DB_NAME)
    try:
        df.to_sql(
            table,
            conn,
            if_exists="replace",
            index=False,
        )
    finally:
        conn.close()

    return table, len(df)


def ingest_path(path):
    """
    Dispatch a single saved file to the right store.

    Returns a dict describing what happened so the UI can show feedback.
    """
    lower = path.lower()

    if lower.endswith(DOC_EXTS):
        n = ingest_document(path)
        return {
            "kind": "document",
            "path": path,
            "chunks": n,
            "ok": n > 0,
        }

    if lower.endswith(DATA_EXTS):
        table, rows = ingest_dataset(path)
        return {
            "kind": "dataset",
            "path": path,
            "table": table,
            "rows": rows,
            "ok": True,
        }

    return {
        "kind": "skipped",
        "path": path,
        "ok": False,
    }


def save_uploaded_file(uploaded_file, folder=KNOWLEDGE_BASE):
    """Persist a Streamlit UploadedFile to disk and return its path."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path
