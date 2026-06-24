import sqlite3
import pandas as pd

from llm_utils import get_llm
from result_formatter import format_result
from dataset_selector import choose_dataset


def get_schema(table_name):

    conn = sqlite3.connect(
        "knowledge.db"
    )

    schema_df = pd.read_sql_query(
        f"PRAGMA table_info({table_name})",
        conn
    )

    conn.close()

    return schema_df


def generate_sql(
    question,
    table_name
):

    schema_df = get_schema(
        table_name
    )

    schema_text = "\n".join(
        [
            f"{row['name']} ({row['type']})"
            for _, row
            in schema_df.iterrows()
        ]
    )

    prompt = f"""
You are an expert SQLite analyst.

Table:
{table_name}

Columns:
{schema_text}

Examples:

Question:
What is the average mileage of electric cars?

SQL:
SELECT AVG(Mileage)
FROM {table_name}
WHERE Fuel_Type = 'Electric';

Question:
What is the most expensive car?

SQL:
SELECT *
FROM {table_name}
ORDER BY Price DESC
LIMIT 1;

Question:
Compare average mileage across fuel types

SQL:
SELECT Fuel_Type,
AVG(Mileage) AS Avg_Mileage
FROM {table_name}
GROUP BY Fuel_Type;

Question:
Compare average mileage across fuel types

SQL:
SELECT Fuel_Type,
AVG(Mileage) AS Avg_Mileage
FROM car_dataset_india
GROUP BY Fuel_Type;

Rules:

- Return EXACTLY ONE SQL query.
- Return SQL ONLY.
- Do NOT explain.
- Do NOT use markdown.
- Do NOT use ```sql.
- Do NOT add comments.
- Do NOT add text before or after the query.
- The first character of the response must be SELECT.

Question:
{question}
"""
    print("\nGenerating SQL...")
    response = get_llm().invoke(prompt)
    print("\nLLM Finished")

    sql = (
        response.content
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )
    import re

    match = re.search(
            r"SELECT[\s\S]*?;",
            sql,
            re.IGNORECASE
        )

    if match:
            sql = match.group(0)


    return sql


def run_sql_analysis(question):
    print("\nSQL QUESTION RECEIVED:")
    print(question)

    table_name = choose_dataset(
        question
    )

    sql = generate_sql(
        question,
        table_name
    )

    print("\nSelected Table:")
    print(table_name)

    print("\nGenerated SQL:")
    print(sql)

    conn = sqlite3.connect(
        "knowledge.db"
    )

    try:

        result_df = pd.read_sql_query(
            sql,
            conn
        )

    except Exception as e:

        conn.close()

        return {
            "error": str(e),
            "sql": sql
        }

    conn.close()

    rows = result_df.to_dict(
        orient="records"
    )

    return {
        "table": table_name,
        "sql": sql,
        "rows": format_result(rows)
    }


if __name__ == "__main__":

    while True:

        question = input(
            "\nQuestion: "
        )

        if question.lower() == "exit":
            break

        result = run_sql_analysis(
            question
        )

        print("\nResult:\n")

        print(result)