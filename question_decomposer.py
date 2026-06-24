from llm_utils import get_llm


def decompose_question(question):

    prompt = f"""
You are a query decomposition agent.

Split the user's question into:

RAG QUESTION:
- Document/report related part only.

SQL QUESTION:
- Structured data related part only.

Rules:

- Do NOT add new analysis.
- Do NOT expand the question.
- Do NOT invent metrics.
- Preserve the user's original intent.
- Return only the minimum question needed.

Question:
{question}

Output format:

RAG QUESTION:
...

SQL QUESTION:
...
"""

    response = get_llm().invoke(prompt)

    return response.content