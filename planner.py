from llm_utils import get_llm, strip_think


def plan_question(question):

    prompt = f"""
You are a query planning agent.

Available tools:

RAG
- Reports
- PDFs
- PPTs
- DOCX files
- Market research
- Trends
- Drivers
- Barriers
- Opportunities
- Risks

SQL
- CSV files
- XLSX files
- Numerical analysis
- Aggregations
- Counts
- Averages
- Maximums
- Minimums
- Comparisons
- Statistics

CHART
- Comparisons
- Trends
- Grouped data
- Visualizations

Examples:

Question:
What are barriers to EV adoption?

RAG: YES
SQL: NO
CHART: NO

Question:
What is average mileage of electric cars?

RAG: NO
SQL: YES
CHART: NO

Question:
Compare average mileage across fuel types

RAG: NO
SQL: YES
CHART: YES

Question:
What are EV adoption trends and average mileage of electric cars?

RAG: YES
SQL: YES
CHART: YES

Return EXACTLY:

RAG: YES/NO
SQL: YES/NO
CHART: YES/NO

Question:
{question}
"""

    response = get_llm().invoke(prompt)

    return strip_think(response.content).strip()


if __name__ == "__main__":

    while True:

        question = input("\nQuestion: ")

        if question.lower() == "exit":
            break

        print("\nPLAN:\n")

        print(
            plan_question(question)
        )