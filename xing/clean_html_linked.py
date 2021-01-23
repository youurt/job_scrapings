import re
import pandas as pd

df = pd.read_csv("linkedin_joined.csv")


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace("\n", "")
    cleantext = cleantext.replace("\t", "")
    return cleantext.strip()


df["text"] = df["text"].apply(lambda x: cleanhtml(x))
df["text"] = df["text"].str.lower()

df = df[df["text"].str.contains(
    'php|/^java$/|senior|werkstudent', regex=True) == False]

df.to_csv("linkedin_cleaned.csv", index=False)
