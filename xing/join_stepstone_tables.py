import pandas as pd


def join_tables():
    df1 = pd.read_csv("stepstone_text.csv")
    df2 = pd.read_csv("stepstone_raw.csv")
    new_df = pd.merge(df1, df2, on="link")
    new_df.to_csv("stepstone_joined.csv", index=False)


join_tables()
