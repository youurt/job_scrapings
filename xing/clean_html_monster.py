import pandas as pd
import re

df = pd.read_csv("monster.csv")


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace("\n", "")
    cleantext = cleantext.replace("\t", "")
    cleantext = cleantext.replace("\r", "")
    return cleantext.strip()


df["description"] = df["description"].apply(lambda x: cleanhtml(x))
df["description"] = df["description"].str.lower()
df["title"] = df["title"].str.lower()
df = df[df["title"].str.contains(
    'php|/^java$/|senior|werkstudent|c#|.net', regex=True) == False]
df = df[df["description"].str.contains(
    'php|/^java$/|senior|werkstudent|c#|.net', regex=True) == False]
df.to_csv("monster_cleaned.csv", index=False)
