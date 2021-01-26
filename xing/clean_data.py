import pandas as pd
import sys


def clean_df(csv_file):
    """
    ARG1: MONTH_BOOL
    """

    df = pd.read_csv(csv_file)

    df["job_title"] = df["job_title"].str.lower()
    df["job_title"] = df["job_title"].str.lower()
    # df["location"] = df["location"].str.lower()

    # df = df[df["position"].str.contains(
    #     'php|/^java$/|sap|.net|c#', regex=True) == False]
    # df.to_csv("res_glassdoor.csv", index=False)


clean_df("linkedin_raw.csv")
