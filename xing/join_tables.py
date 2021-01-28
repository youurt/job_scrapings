import sys
import pandas as pd


def join_tables():
    """
    ARG1: Name of Site
    ARG2: Topic
    """

    df1 = pd.read_csv(
        f"data_{sys.argv[2]}/{sys.argv[1]}/{sys.argv[1]}_text.csv")

    df2 = pd.read_csv(
        f"data_{sys.argv[2]}/{sys.argv[1]}/{sys.argv[1]}_raw.csv")

    new_df = pd.merge(df1, df2, on="job_id")
    new_df.to_csv(
        f"data_{sys.argv[2]}/{sys.argv[1]}/{sys.argv[1]}_joined.csv", index=False)


join_tables()
