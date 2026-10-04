
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "healthcare_claims_clean.csv"
)

df = pd.read_csv(INPUT_FILE)

print("=" * 55)
print("HEALTHCARE CLAIMS - BUSINESS VALIDATION")
print("=" * 55)

# 1. Check the relationship between claim status and outcome
print("\n1. Claim status vs outcome:")
print(pd.crosstab(df["claim_status"], df["outcome"]))

# 2. Check financial totals
print("\n2. Financial summary:")
print(
    df[["billed_amount", "allowed_amount", "paid_amount",
        "outstanding_amount"]].sum().round(2)
)

# 3. Check whether outstanding amount matches allowed minus paid
expected_outstanding = df["allowed_amount"] - df["paid_amount"]

difference = (
    expected_outstanding - df["outstanding_amount"]
).abs()

print("\n3. Outstanding amount calculation check:")
print("Rows with mismatched outstanding amount:", int((difference > 0.01).sum()))

# 4. Check claims marked Paid that still have an outstanding amount
paid_status = df[df["claim_status"] == "Paid"]

print("\n4. Claims with Paid status:")
print("Total claims:", len(paid_status))
print(
    "Claims with outstanding amount above zero:",
    int((paid_status["outstanding_amount"] > 0).sum())
)

# 5. Check denied claims with positive paid amounts
denied_status = df[df["claim_status"] == "Denied"]

print("\n5. Denied claims with positive paid amounts:")
print(
    int((denied_status["paid_amount"] > 0).sum()),
    "out of",
    len(denied_status)
)

# 6. Check follow-up among denied claims
print("\n6. Follow-up requirement for denied claims:")
print(denied_status["follow_up_required"].value_counts(dropna=False))

print("\nBusiness validation completed.")