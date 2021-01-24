import pandas as pd


def clean_df(csv_file):
    df = pd.read_csv(csv_file)
    df["title"] = df["title"].str.lower()
    df["activated"] = df["activated"].str.lower()
    df["location"] = df["location"].str.lower()

    df = df[df["activated"].str.contains('30') == False]
    df = df[df["title"].str.contains(
        'php|/^java$/|senior|werkstudent|sap', regex=True) == False]
    df.to_csv("res_indeed.csv", index=False)


clean_df("indeed_raw.csv")
