
from pathlib import Path

import pandas as pd

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "raw" / "healthcare_claims_export.csv"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "healthcare_claims_clean.csv"

# Load the exported dataset
df = pd.read_csv(INPUT_FILE)

print("Original shape:", df.shape)

# 1. Standardize column names

# 1. Remove MongoDB's technical ID before renaming columns
if "_id" in df.columns:
    df = df.drop(columns=["_id"])

# 2. Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

# 3. Remove fully duplicated records
full_duplicates = int(df.duplicated().sum())
df = df.drop_duplicates().copy()

print("Fully duplicated rows removed:", full_duplicates)

# 4. Standardize text columns
for column in df.select_dtypes(include=["object", "string"]).columns:
    df[column] = df[column].astype("string").str.strip()
    df[column] = df[column].replace("", pd.NA)

# 5. Convert monetary fields to numeric
money_columns = [
    "billed_amount",
    "allowed_amount",
    "paid_amount",
]

for column in money_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# 6. Parse service dates
df["date_of_service"] = pd.to_datetime(
    df["date_of_service"],
    format="mixed",
    errors="coerce",
    dayfirst=False
)

# 7. Report missing values after conversion
print("\nMissing values after type conversion:")
print(df.isna().sum().to_string())

# 8. Check for invalid monetary amounts
for column in money_columns:
    invalid_count = int((df[column] < 0).fillna(False).sum())
    print(f"Negative values in {column}: {invalid_count}")

# 9. Check financial relationships
print("\nFinancial validation checks:")
print(
    "Paid > allowed:",
    int((df["paid_amount"] > df["allowed_amount"]).fillna(False).sum())
)
print(
    "Allowed > billed:",
    int((df["allowed_amount"] > df["billed_amount"]).fillna(False).sum())
)

# 10. Check business-key duplicates
if "claim_id" in df.columns:
    print(
        "\nRows with duplicate claim IDs:",
        int(df["claim_id"].duplicated(keep=False).sum())
    )

# 11. Derive outstanding amount
df["outstanding_amount"] = (
    df["allowed_amount"] - df["paid_amount"]
)

# Flag records that need investigation; do not silently delete them
df["data_quality_flag"] = (
    df[money_columns].isna().any(axis=1)
    | df["date_of_service"].isna()
    | (df[money_columns] < 0).any(axis=1)
    | (df["paid_amount"] > df["allowed_amount"])
    | (df["allowed_amount"] > df["billed_amount"])
)

# 12. Save the validated working copy
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("\nFinal shape:", df.shape)
print("Rows flagged for review:", int(df["data_quality_flag"].sum()))
print("Cleaned dataset saved to:", OUTPUT_FILE)
print("Source CSV and MongoDB records were not modified.")