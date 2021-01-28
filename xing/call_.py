import subprocess
import sys

for doc in ["glassdoor", "indeed", "linkedin", "stepstone"]:
    subprocess.call(["python", "join_tables.py", doc, sys.argv[1]])

for document in ["glassdoor", "indeed", "linkedin", "monster", "stepstone", "xing"]:
    subprocess.call(["python", "clean_data.py", document, sys.argv[1]])
