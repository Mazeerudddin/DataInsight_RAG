import os
import pandas as pd
import matplotlib.pyplot as plt


def generate_chart(sql_result):

    rows = sql_result["rows"]

    if isinstance(rows, dict):
        return None

    if len(rows) < 2:
        return None

    df = pd.DataFrame(rows)

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_cols = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    os.makedirs(
        "charts",
        exist_ok=True
    )

    chart_path = (
        "charts/latest_chart.png"
    )

    # BAR CHART

    if (
        len(categorical_cols) >= 1
        and
        len(numeric_cols) >= 1
    ):

        x_col = categorical_cols[0]
        y_col = numeric_cols[0]

        plt.figure(
            figsize=(10, 6)
        )

        plt.bar(
            df[x_col],
            df[y_col]
        )

        plt.xlabel(x_col)

        plt.ylabel(y_col)

        plt.title(
            f"{y_col} by {x_col}"
        )

        plt.xticks(
            rotation=45
        )

        plt.tight_layout()

        plt.savefig(
            chart_path,
            bbox_inches="tight"
        )

        plt.close()

        return chart_path

    # SCATTER CHART

    if len(numeric_cols) >= 2:

        x_col = numeric_cols[0]
        y_col = numeric_cols[1]

        plt.figure(
            figsize=(10, 6)
        )

        plt.scatter(
            df[x_col],
            df[y_col]
        )

        plt.xlabel(x_col)

        plt.ylabel(y_col)

        plt.title(
            f"{y_col} vs {x_col}"
        )

        plt.tight_layout()

        plt.savefig(
            chart_path,
            bbox_inches="tight"
        )

        plt.close()

        return chart_path

    return None