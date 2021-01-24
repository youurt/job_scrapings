import pandas as pd

df = pd.read_csv("stepstone_joined.csv")


df["text"] = df["text"].str.lower()
df = df[df["text"].str.contains(
    'php|/^java$/|senior|werkstudent|sap|c#|.net|lead', regex=True) == False]
df.to_csv("stepstone_cleaned.csv", index=False)
