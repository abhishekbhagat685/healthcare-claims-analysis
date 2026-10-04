import os
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

# Load project .env
project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

csv_path = project_root / "data" / "processed" / "healthcare_claims_clean.csv"

if not csv_path.exists():
    raise FileNotFoundError(f"CSV not found: {csv_path}")

# Read the complete cleaned CSV
df = pd.read_csv(csv_path, encoding="utf-8-sig")
df = df.where(pd.notna(df), None)

print("CSV rows:", len(df))
print("CSV columns:", len(df.columns))

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE", "healthcare_claims_db"),
)

cursor = connection.cursor()

# Use a separate table to protect your existing imported data
table_name = "healthcare_claims_vscode"

columns = [
    "claim_id", "provider_id", "patient_id", "date_of_service",
    "billed_amount", "procedure_code", "diagnosis_code",
    "allowed_amount", "paid_amount", "insurance_type",
    "claim_status", "reason_code", "follow_up_required",
    "ar_status", "outcome", "outstanding_amount",
    "data_quality_flag"
]

# Validate expected columns
if list(df.columns) != columns:
    raise ValueError(
        f"Unexpected CSV columns. Found: {list(df.columns)}"
    )

# Create a fresh destination table
cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")

cursor.execute("""
CREATE TABLE healthcare_claims_vscode (
    claim_id VARCHAR(100),
    provider_id VARCHAR(100),
    patient_id VARCHAR(100),
    date_of_service DATE,
    billed_amount DECIMAL(12,2),
    procedure_code VARCHAR(100),
    diagnosis_code VARCHAR(100),
    allowed_amount DECIMAL(12,2),
    paid_amount DECIMAL(12,2),
    insurance_type VARCHAR(100),
    claim_status VARCHAR(100),
    reason_code VARCHAR(255),
    follow_up_required VARCHAR(20),
    ar_status VARCHAR(100),
    outcome VARCHAR(100),
    outstanding_amount DECIMAL(12,2),
    data_quality_flag VARCHAR(255)
)
""")

insert_sql = """
INSERT INTO healthcare_claims_vscode (
    claim_id, provider_id, patient_id, date_of_service,
    billed_amount, procedure_code, diagnosis_code,
    allowed_amount, paid_amount, insurance_type,
    claim_status, reason_code, follow_up_required,
    ar_status, outcome, outstanding_amount, data_quality_flag
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s
)
"""

try:
    rows = []
    for record in df.itertuples(index=False, name=None):
        rows.append(tuple(
            value.to_pydatetime() if hasattr(value, "to_pydatetime")
            else value
            for value in record
        ))

    cursor.executemany(insert_sql, rows)
    connection.commit()

    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
    imported_count = cursor.fetchone()[0]

    print("Rows in CSV:", len(df))
    print("Rows inserted:", cursor.rowcount)
    print("Rows verified in MySQL:", imported_count)

    if imported_count != len(df):
        raise RuntimeError("Imported row count does not match CSV row count.")

    print("IMPORT SUCCESSFUL")

except Exception:
    connection.rollback()
    raise

finally:
    cursor.close()
    connection.close()