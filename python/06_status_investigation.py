
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

print("=" * 60)
print("CLAIM STATUS INVESTIGATION")
print("=" * 60)

# Payment and balance summary by claim status
print("\n1. Financial metrics by claim status:")

print(
    df.groupby("claim_status")
    .agg(
        claim_count=("claim_id", "count"),
        total_allowed=("allowed_amount", "sum"),
        total_paid=("paid_amount", "sum"),
        total_outstanding=("outstanding_amount", "sum"),
        claims_with_zero_balance=(
            "outstanding_amount",
            lambda s: (s == 0).sum()
        ),
        claims_with_positive_balance=(
            "outstanding_amount",
            lambda s: (s > 0).sum()
        )
    )
    .round(2)
)

# Inspect outcome patterns without printing individual claim records
print("\n2. Outcome distribution by claim status (% within status):")

status_outcome_pct = pd.crosstab(
    df["claim_status"],
    df["outcome"],
    normalize="index"
) * 100

print(status_outcome_pct.round(2))

# Check payment amount against allowed amount
print("\n3. Payment amount checks:")

print(
    "Rows where paid amount equals allowed amount:",
    int((df["paid_amount"] == df["allowed_amount"]).sum())
)

print(
    "Rows where paid amount is below allowed amount:",
    int((df["paid_amount"] < df["allowed_amount"]).sum())
)

print(
    "Rows where paid amount is zero:",
    int((df["paid_amount"] == 0).sum())
)

print("\nInvestigation completed.")


print("\n7. Balance summary by claim status:")

balance_summary = df.groupby("claim_status").agg(
    total_claims=("claim_id", "count"),
    zero_balance=("outstanding_amount", lambda s: (s == 0).sum()),
    positive_balance=("outstanding_amount", lambda s: (s > 0).sum()),
    total_outstanding=("outstanding_amount", "sum"),
    average_outstanding=("outstanding_amount", "mean")
)

print(balance_summary.round(2).to_string())