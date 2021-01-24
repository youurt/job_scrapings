import pandas as pd


def clean_df(csv_file):
    df = pd.read_csv(csv_file)
    df["title"] = df["title"].str.lower()

    df = df[df["title"].str.contains(
        'php|/^java$/|senior|werkstudent|sap', regex=True) == False]
    df.to_csv("res_stepstone.csv", index=False)


clean_df("stepstone_raw.csv")
