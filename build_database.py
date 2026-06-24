import sqlite3

from dataset_registry import datasets


DB_NAME = "knowledge.db"


def build_database():

    conn = sqlite3.connect(DB_NAME)

    for table_name, df in datasets.items():

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        print(
            f"Loaded table: {table_name}"
        )

    conn.close()

    print(
        f"\nDatabase created: {DB_NAME}"
    )


if __name__ == "__main__":

    build_database()