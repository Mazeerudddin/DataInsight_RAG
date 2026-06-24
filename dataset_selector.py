import sqlite3

from llm_utils import get_llm, strip_think


def get_table_catalog():

    conn = sqlite3.connect(
        "knowledge.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    )

    tables = [
        row[0]
        for row in cursor.fetchall()
    ]

    catalog = []

    for table in tables:

        cursor.execute(
            f"PRAGMA table_info({table})"
        )

        columns = [
            row[1]
            for row
            in cursor.fetchall()
        ]

        catalog.append(
            {
                "table": table,
                "columns": columns
            }
        )

    conn.close()

    return catalog


def choose_dataset(question):

    catalog = get_table_catalog()

    catalog_text = ""

    for item in catalog:

        catalog_text += (
            f"\nTable: {item['table']}\n"
        )

        catalog_text += (
            "Columns: "
            + ", ".join(item["columns"])
            + "\n"
        )

    prompt = f"""
You are a database routing expert.

Available tables:

{catalog_text}

Question:
{question}

Rules:

- Return ONLY the table name.
- No explanation.
- No markdown.

Answer:
"""

    response = get_llm().invoke(prompt)

    table_name = (
        strip_think(response.content)
        .replace("`", "")
        .strip()
    )

    return table_name


if __name__ == "__main__":

    while True:

        question = input(
            "\nQuestion: "
        )

        if question.lower() == "exit":
            break

        table = choose_dataset(
            question
        )

        print(
            "\nSelected Table:"
        )

        print(table)