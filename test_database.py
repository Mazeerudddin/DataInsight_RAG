import sqlite3


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

tables = cursor.fetchall()

print("\nTables Found:\n")

for table in tables:

    print(table[0])

conn.close()