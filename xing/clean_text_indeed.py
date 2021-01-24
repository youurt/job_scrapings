import pandas as pd
import re

df = pd.read_csv("indeed_joined.csv")


df["text"] = df["text"].str.lower()
df = df[df["text"].str.contains(
    'php|/^java$/|senior|werkstudent|sap|c#|.net|lead', regex=True) == False]
df.to_csv("indeed_cleaned.csv", index=False)
