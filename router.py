from llm_utils import get_llm, strip_think


def route_question(question):

    prompt = f"""
You are a routing agent.

Routes:

rag
- Reports
- PDFs
- Research questions
- Market trends
- Drivers
- Barriers

sql
- Single numerical calculations
- Counts
- Averages
- Maximums
- Minimums

chart
- Comparisons
- Grouped analysis
- Visualizations
- Compare X across Y
- Trends over categories

hybrid
- Requires both document research and structured data analysis

Examples:

Question:
What are barriers to EV adoption?
Answer:
rag

Question:
What is average mileage of electric cars?
Answer:
sql

Question:
Compare average mileage across fuel types
Answer:
chart

Question:
What are EV adoption trends and average mileage of electric cars?
Answer:
hybrid

Return ONLY:

rag
sql
chart
hybrid

Question:
{question}
"""

    response = get_llm().invoke(
        prompt
    )

    return (
        strip_think(response.content)
        .strip()
        .lower()
    )


if __name__ == "__main__":

    while True:

        q = input(
            "\nQuestion: "
        )

        print(
            route_question(q)
        )