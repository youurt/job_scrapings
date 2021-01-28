import pandas as pd

df = pd.read_csv("glassdoor_cleaned_lab.csv", sep=';')
print(df["label"])
