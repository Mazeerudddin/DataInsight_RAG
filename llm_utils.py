"""LLM utilities and centralized instance management."""

import re
from langchain_ollama import ChatOllama

_THINK_RE = re.compile(
    r"<think>.*?</think>",
    re.DOTALL | re.IGNORECASE,
)

_llm_instance = None

def get_llm():
    """Get or create the singleton LLM instance."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatOllama(
            model="qwen3:8b",
            temperature=0
        )
    return _llm_instance

def strip_think(text):
    """Remove <think>...</think> reasoning blocks."""
    if not text:
        return text
    return _THINK_RE.sub("", text).strip()
