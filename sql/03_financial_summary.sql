USE healthcare_claims_db;

-- KPI 3: Financial Summary
-- Purpose: Summarize claim finances overall and by insurance type.

-- Part A: Overall financial summary
SELECT
    COUNT(*) AS total_claims,
    ROUND(SUM(billed_amount), 2) AS total_billed_amount,
    ROUND(SUM(allowed_amount), 2) AS total_allowed_amount,
    ROUND(SUM(paid_amount), 2) AS total_paid_amount,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding_amount,
    ROUND(
        100.0 * SUM(paid_amount) /
        NULLIF(SUM(allowed_amount), 0),
        2
    ) AS paid_to_allowed_percentage
FROM healthcare_claims_vscode;


-- Part B: Financial summary by insurance type
SELECT
    insurance_type,
    COUNT(*) AS total_claims,
    ROUND(SUM(billed_amount), 2) AS total_billed_amount,
    ROUND(SUM(allowed_amount), 2) AS total_allowed_amount,
    ROUND(SUM(paid_amount), 2) AS total_paid_amount,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding_amount
FROM healthcare_claims_vscode
GROUP BY insurance_type
ORDER BY total_outstanding_amount DESC;