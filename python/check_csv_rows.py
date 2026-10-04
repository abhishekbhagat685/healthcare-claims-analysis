import pandas as pd
from pathlib import Path

file_path = Path("data/processed/healthcare_claims_clean.csv")

print("CSV exists:", file_path.exists())

if file_path.exists():
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    print("Data rows:", len(df))
    print("Columns:", len(df.columns))
    print("First column:", df.columns[0])