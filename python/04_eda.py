

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. PROJECT PATHS AND DATA LOADING
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR / "data" / "processed" / "healthcare_claims_clean.csv"
)

OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
CHART_DIR = PROJECT_DIR / "screenshots"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("HEALTHCARE CLAIMS ANALYSIS - EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\nDataset shape:", df.shape)


# --------------------------------------------------
# 2. CLAIM STATUS SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("CLAIM STATUS SUMMARY")
print("=" * 60)

claim_status_counts = df["claim_status"].value_counts(dropna=False)
print(claim_status_counts)

print("\nClaim status percentage:")
print(
    (df["claim_status"].value_counts(normalize=True, dropna=False) * 100)
    .round(2)
)


# --------------------------------------------------
# 3. INSURANCE TYPE SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("INSURANCE TYPE SUMMARY")
print("=" * 60)

insurance_counts = df["insurance_type"].value_counts(dropna=False)
print(insurance_counts)

print("\nInsurance type percentage:")
print(
    (df["insurance_type"].value_counts(normalize=True, dropna=False) * 100)
    .round(2)
)


# --------------------------------------------------
# 4. OUTSTANDING AMOUNT BY CLAIM STATUS
# --------------------------------------------------

print("\n" + "=" * 60)
print("OUTSTANDING AMOUNT BY CLAIM STATUS")
print("=" * 60)

status_outstanding = (
    df.groupby("claim_status", dropna=False)["outstanding_amount"]
    .agg(["count", "sum", "mean"])
    .round(2)
    .sort_values("sum", ascending=False)
)

print(status_outstanding)


# --------------------------------------------------
# 5. OUTSTANDING AMOUNT BY INSURANCE TYPE
# --------------------------------------------------

print("\n" + "=" * 60)
print("OUTSTANDING AMOUNT BY INSURANCE TYPE")
print("=" * 60)

insurance_outstanding = (
    df.groupby("insurance_type", dropna=False)["outstanding_amount"]
    .agg(["count", "sum", "mean"])
    .round(2)
    .sort_values("sum", ascending=False)
)

print(insurance_outstanding)


# --------------------------------------------------
# 6. FOLLOW-UP REQUIREMENT
# --------------------------------------------------

print("\n" + "=" * 60)
print("FOLLOW-UP REQUIREMENT")
print("=" * 60)

follow_up_counts = df["follow_up_required"].value_counts(dropna=False)
print(follow_up_counts)

print("\nFollow-up percentage:")
print(
    (
        df["follow_up_required"].value_counts(
            normalize=True, dropna=False
        ) * 100
    ).round(2)
)


# --------------------------------------------------
# 7. OUTCOME SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("OUTCOME SUMMARY")
print("=" * 60)

outcome_counts = df["outcome"].value_counts(dropna=False)
print(outcome_counts)

print("\nOutcome percentage:")
print(
    (df["outcome"].value_counts(normalize=True, dropna=False) * 100)
    .round(2)
)


# --------------------------------------------------
# 8. CLAIM STATUS VS OUTCOME
# --------------------------------------------------

print("\n" + "=" * 60)
print("CLAIM STATUS VS OUTCOME")
print("=" * 60)

status_outcome_table = pd.crosstab(
    df["claim_status"],
    df["outcome"],
    margins=True,
    dropna=False
)

print(status_outcome_table)


# --------------------------------------------------
# 9. REASON CODES AMONG DENIED CLAIMS
# --------------------------------------------------

print("\n" + "=" * 60)
print("TOP REASON CODES AMONG DENIED CLAIMS")
print("=" * 60)

denied_claims = df[df["claim_status"] == "Denied"]

if denied_claims.empty:
    print("No denied claims found.")
else:
    denied_reason_counts = (
        denied_claims["reason_code"]
        .fillna("Missing reason code")
        .value_counts()
        .head(10)
    )

    print("Total denied claims:", len(denied_claims))
    print(denied_reason_counts)


# --------------------------------------------------
# 10. CHART 1: CLAIM STATUS DISTRIBUTION
# --------------------------------------------------

status_counts = df["claim_status"].value_counts()

plt.figure(figsize=(9, 5))
status_counts.plot(kind="bar")
plt.title("Healthcare Claims by Status")
plt.xlabel("Claim Status")
plt.ylabel("Number of Claims")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(CHART_DIR / "01_claim_status.png", dpi=150)
plt.close()


# --------------------------------------------------
# 11. CHART 2: OUTSTANDING BY INSURANCE TYPE
# --------------------------------------------------

insurance_chart_data = (
    df.groupby("insurance_type")["outstanding_amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
insurance_chart_data.plot(kind="bar")
plt.title("Outstanding Amount by Insurance Type")
plt.xlabel("Insurance Type")
plt.ylabel("Outstanding Amount")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(
    CHART_DIR / "02_outstanding_by_insurance.png",
    dpi=150
)
plt.close()


# --------------------------------------------------
# 12. CHART 3: FOLLOW-UP REQUIREMENT
# --------------------------------------------------

follow_up_chart_data = df["follow_up_required"].value_counts()

plt.figure(figsize=(7, 5))
follow_up_chart_data.plot(kind="bar")
plt.title("Claims by Follow-up Requirement")
plt.xlabel("Follow-up Required")
plt.ylabel("Number of Claims")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(CHART_DIR / "03_follow_up_required.png", dpi=150)
plt.close()


# --------------------------------------------------
# 13. CHART 4: TOP DENIAL REASON CODES
# --------------------------------------------------

if not denied_claims.empty:
    reason_chart_data = (
        denied_claims["reason_code"]
        .fillna("Missing reason code")
        .value_counts()
        .head(10)
    )

    plt.figure(figsize=(10, 6))
    reason_chart_data.plot(kind="bar")
    plt.title("Top Reason Codes Among Denied Claims")
    plt.xlabel("Reason Code")
    plt.ylabel("Number of Denied Claims")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(
        CHART_DIR / "04_denial_reason_codes.png",
        dpi=150
    )
    plt.close()


# --------------------------------------------------
# 14. COMPLETION MESSAGE
# --------------------------------------------------

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)

print("Rows analyzed:", len(df))
print("Charts saved in:", CHART_DIR)
print("Source dataset was not modified.")