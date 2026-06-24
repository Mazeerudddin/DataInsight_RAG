def format_result(rows):

    if not rows:

        return {
            "result": "No data found"
        }

    if len(rows) == 1:

        row = rows[0]

        if len(row) == 1:

            return {
                "result": list(
                    row.values()
                )[0]
            }

    return rows