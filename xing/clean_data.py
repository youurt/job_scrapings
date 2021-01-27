import re
import pandas as pd
import sys

"""
    ARG1: Name of Site
    ARG2: Topic
"""


df = pd.read_csv(f"data_{sys.argv[2]}/{sys.argv[1]}/{sys.argv[1]}_joined.csv")


def cleanhtml(raw_html):

    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace("\n", "")
    cleantext = cleantext.replace("\t", "")
    return cleantext.strip().lower()


df["text"] = df["text"].astype(str).apply(lambda x: cleanhtml(x))


df = df[df["text"].str.contains(
    'php|/^java$/|sap|.net|c#', regex=True) == False]

df.to_csv(
    f"data_{sys.argv[2]}/{sys.argv[1]}/{sys.argv[1]}_cleaned.csv", index=False)
