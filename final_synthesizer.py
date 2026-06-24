from llm_utils import get_llm, strip_think


def synthesize_answer(
    question,
    tool_outputs,
    conversation_context=""
):

    rag_findings = ""

    sql_findings = ""

    citations = ""

    if "rag" in tool_outputs:

        rag_findings = tool_outputs[
            "rag"
        ].get(
            "answer",
            ""
        )

        if "citations" in tool_outputs[
            "rag"
        ]:

            citation_lines = []

            for c in tool_outputs[
                "rag"
            ]["citations"]:

                citation_lines.append(
                    f"- {c['source']} (Page {c['page']})"
                )

            citations = "\n".join(
                citation_lines
            )

    if "sql" in tool_outputs:

        sql_findings = str(
            tool_outputs[
                "sql"
            ].get(
                "rows",
                ""
            )
            )
    print("\nRAG FINDINGS:")
    print(rag_findings)

    print("\nSQL FINDINGS:")
    print(sql_findings)
    prompt = f"""
You are an AI research copilot.

Conversation History:

{conversation_context}

Question:

{question}

RAG Findings:

{rag_findings}

SQL Findings:

{sql_findings}

Sources:

{citations}

Rules:

- Use BOTH RAG and SQL findings.
- If SQL contains numerical values,
  explicitly mention them.
- If RAG findings exist,
  summarize them.
- Do not say information is unavailable
  if SQL findings contain it.
- Do not invent facts.
- End with Sources if provided.
- Never infer units.
- Use only units explicitly present in the data.

Answer:
"""

    response = get_llm().invoke(
        prompt
    )

    return strip_think(response.content)