import pandas as pd


def clean_df(csv_file):
    df = pd.read_csv(csv_file)
    df["job_name"] = df["job_name"].str.lower()
    df["list_date"] = df["list_date"].str.lower()
    df["location"] = df["location"].str.lower()

    df = df[df["list_date"].str.contains('month|months') == False]
    df = df[df["job_name"].str.contains(
        'php|/^java$/|senior|werkstudent', regex=True) == False]
    df.to_csv("res.csv", index=False)


clean_df("linkedin_raw.csv")
