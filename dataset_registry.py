import os
import pandas as pd


def load_datasets(folder="knowledge_base"):

    datasets = {}

    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        return datasets

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        try:

            if file.endswith(".csv"):

                name = os.path.splitext(file)[0]

                datasets[name] = pd.read_csv(path)

                print(f"Loaded CSV: {file}")

            elif file.endswith(".xlsx"):

                name = os.path.splitext(file)[0]

                datasets[name] = pd.read_excel(path)

                print(f"Loaded XLSX: {file}")

        except Exception as e:

            print(f"Failed to load {file}")
            print(e)

    return datasets


datasets = load_datasets()


if __name__ == "__main__":

    print("\n===== DATASETS =====")

    for name, df in datasets.items():

        print(f"\nDataset: {name}")

        print("Rows:", len(df))

        print("Columns:")

        for col in df.columns:
            print("-", col)