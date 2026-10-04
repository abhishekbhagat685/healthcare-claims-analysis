
USE healthcare_claims_db;

-- KPI 12: Final Data Validation
-- Purpose: Verify row counts, unique claim IDs, missing values,
-- and financial consistency.

-- Query 1: Row count and required-field validation
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT claim_id) AS unique_claims,
    SUM(CASE WHEN claim_id IS NULL THEN 1 ELSE 0 END)
        AS missing_claim_ids,
    SUM(CASE WHEN date_of_service IS NULL THEN 1 ELSE 0 END)
        AS missing_service_dates,
    SUM(CASE WHEN outstanding_amount IS NULL THEN 1 ELSE 0 END)
        AS missing_outstanding_amounts
FROM healthcare_claims_vscode;

-- Query 2: Check duplicate claim IDs
SELECT
    claim_id,
    COUNT(*) AS occurrences
FROM healthcare_claims_vscode
GROUP BY claim_id
HAVING COUNT(*) > 1;

-- Query 3: Check financial consistency
-- Assumption: Outstanding = Allowed Amount - Paid Amount.
SELECT
    COUNT(*) AS total_claims,
    SUM(
        CASE
            WHEN ROUND(outstanding_amount, 2)
                 <> ROUND(allowed_amount - paid_amount, 2)
            THEN 1
            ELSE 0
        END
    ) AS financial_mismatch_count,
    ROUND(
        SUM(outstanding_amount - (allowed_amount - paid_amount)),
        2
    ) AS reconciliation_difference
FROM healthcare_claims_vscode;

-- Query 4: Check for negative financial values
SELECT
    SUM(CASE WHEN billed_amount < 0 THEN 1 ELSE 0 END)
        AS negative_billed_amounts,
    SUM(CASE WHEN allowed_amount < 0 THEN 1 ELSE 0 END)
        AS negative_allowed_amounts,
    SUM(CASE WHEN paid_amount < 0 THEN 1 ELSE 0 END)
        AS negative_paid_amounts,
    SUM(CASE WHEN outstanding_amount < 0 THEN 1 ELSE 0 END)
        AS negative_outstanding_amounts
FROM healthcare_claims_vscode;