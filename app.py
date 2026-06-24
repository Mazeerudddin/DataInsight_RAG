from router import route_question
from rag_agent import answer_question
from sql_agent import run_sql_analysis
from final_synthesizer import synthesize_answer
from chart_agent import generate_chart
from memory import ConversationMemory
from question_decomposer import decompose_question

import re

memory = ConversationMemory()


def app(question):

    memory.add_user_message(
        question
    )

    route = route_question(
        question
    )

    print(
        "\n===== ROUTE =====\n"
    )

    print(route)

    results = {}

    if route == "rag":

        print(
            "\nRunning RAG..."
        )

        results["rag"] = (
            answer_question(
                question,
                memory.get_context()
            )
        )
        

    elif route == "sql":

        print(
            "\nRunning SQL..."
        )

        results["sql"] = (
            run_sql_analysis(
                question
            )
        )
        

    elif route == "chart":

        print(
            "\nRunning SQL..."
        )

        results["sql"] = (
            run_sql_analysis(
                question
            )
        )

        print(
            "\nGenerating Chart..."
        )

        chart_path = generate_chart(
            results["sql"]
)

        results["chart"] = chart_path

    elif route == "hybrid":

        decomposition = (
            decompose_question(
                question
            )
        )

        print(
            "\n===== DECOMPOSITION =====\n"
        )

        print(
            decomposition
        )

        rag_match = re.search(
            r"RAG QUESTION:\s*(.*?)\s*SQL QUESTION:",
            decomposition,
            re.DOTALL
        )

        sql_match = re.search(
            r"SQL QUESTION:\s*(.*)",
            decomposition,
            re.DOTALL
        )

        rag_question = (
            rag_match.group(1).strip()
            if rag_match
            else question
        )

        sql_question = (
            sql_match.group(1).strip()
            if sql_match
            else question
        )

        print(
            "\nRAG QUESTION:"
        )
        print(
            rag_question
        )

        print(
            "\nSQL QUESTION:"
        )
        print(
            sql_question
        )

        print(
            "\nRunning RAG..."
        )

        results["rag"] = (
            answer_question(
                rag_question,
                memory.get_context()
            )
        )

        print(
            "\nRunning SQL..."
        )

        results["sql"] = (
            run_sql_analysis(
                sql_question
            )
        )

    conversation_context = (
        memory.get_context()
    )

    final_answer = (
        synthesize_answer(
            question,
            results,
            conversation_context
        )
    )

    memory.add_assistant_message(
        final_answer
    )

    return {
        "answer": final_answer,
        "raw_results": results
    }


if __name__ == "__main__":

    while True:

        question = input(
            "\nQuestion: "
        )

        if question.lower() == "exit":
            break

        result = app(
            question
        )

        print(
            "\n===== FINAL ANSWER =====\n"
        )

        print(
            result["answer"]
        )