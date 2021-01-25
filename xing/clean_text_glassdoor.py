import pandas as pd

df = pd.read_csv("glassdoor_joined.csv")


df["text"] = df["text"].str.lower()
df = df[df["text"].str.contains(
    'php|/^java$/|sap|c#|.net|lead', regex=True) == False]
df.to_csv("glassdoor_cleaned.csv", index=False)
