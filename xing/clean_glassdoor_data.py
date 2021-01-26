import pandas as pd


def clean_df(csv_file):

    df = pd.read_csv(csv_file)
    df["position"] = df["position"].str.lower()
    df["location"] = df["location"].str.lower()

    df = df[df["position"].str.contains(
        'php|/^java$/|sap|.net|c#', regex=True) == False]
    df.to_csv("res_glassdoor.csv", index=False)


clean_df("glassdoor_raw.csv")
