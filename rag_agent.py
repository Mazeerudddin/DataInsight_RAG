from llm_utils import get_llm, strip_think
from query_rewriter import rewrite_query
from retriever import retrieve
from dotenv import load_dotenv

load_dotenv()


def answer_question(
    question,
    conversation_context=""
):
    print("\nRAG QUESTION RECEIVED:")
    print(question)
    search_query = rewrite_query(
    question,
    conversation_context
)

    print(
    "\nRewritten Query:"
)

    print(search_query)
    docs = retrieve(
         search_query,
        k=5
    )
    print(docs)

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    response = get_llm().invoke(
        f"""
You are a research analyst.

Answer ONLY from the provided context.

Do not invent facts.

Context:

{context}

Question:

{question}
"""
    )

    citations = []

    for doc in docs:

        source = doc.metadata.get(
            "source_file",
            "Unknown"
        )

        page = (
            doc.metadata.get(
                "page",
                0
            ) + 1
)

        citations.append(
            {
                "source": source,
                "page": page
            }
        )

    return {
        "answer":
        strip_think(response.content),

        "citations":
        citations
    }