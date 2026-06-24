from llm_utils import get_llm


def rewrite_query(
    question,
    conversation_context=""
):

    prompt = f"""
You are a query rewriting system.

Conversation History:

{conversation_context}

Current Question:

{question}

- Rewrite ONLY the current question.
- Use conversation history only to resolve references.
- Do NOT add unrelated topics from previous messages.
- Do NOT merge multiple questions.
- Return one standalone search query

Rewritten Query:
"""

    response = get_llm().invoke(
        prompt
    )

    return response.content.strip()


if __name__ == "__main__":

    history = """
USER: What are barriers to EV adoption?

ASSISTANT: ...
"""

    print(
        rewrite_query(
            "What about India specifically?",
            history
        )
    )