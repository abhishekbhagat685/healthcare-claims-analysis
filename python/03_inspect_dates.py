
from pathlib import Path
import pandas as pd

project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "raw" / "healthcare_claims_export.csv"

df = pd.read_csv(file_path)

print("Columns:")
print(df.columns.tolist())

print("\nFirst 15 raw Date of Service values:")
print(df["Date of Service"].head(15).to_string(index=False))

print("\nData type:")
print(df["Date of Service"].dtype)

print("\nDistinct date examples:")
print(df["Date of Service"].drop_duplicates().head(20).to_string(index=False))