USE healthcare_claims_db;

-- KPI 6: Insurance-wise Claims Analysis
-- Purpose: Compare claim volumes and financial metrics by insurance type.

-- Part A: Financial summary by insurance type
SELECT
    insurance_type,
    COUNT(*) AS total_claims,
    ROUND(SUM(billed_amount), 2) AS total_billed,
    ROUND(SUM(allowed_amount), 2) AS total_allowed,
    ROUND(SUM(paid_amount), 2) AS total_paid,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding
FROM healthcare_claims_vscode
GROUP BY insurance_type
ORDER BY total_outstanding DESC;


-- Part B: Claim status breakdown by insurance type
SELECT
    insurance_type,
    claim_status,
    COUNT(*) AS total_claims,
    ROUND(
        100.0 * COUNT(*) /
        NULLIF(
            (SELECT COUNT(*)
             FROM healthcare_claims_vscode AS t2
             WHERE t2.insurance_type = t1.insurance_type),
            0
        ),
        2
    ) AS percentage_within_insurance
FROM healthcare_claims_vscode AS t1
GROUP BY insurance_type, claim_status
ORDER BY insurance_type, total_claims DESC;


-- Part C: Denied claims by insurance type
SELECT
    insurance_type,
    COUNT(*) AS denied_claims,
    ROUND(SUM(outstanding_amount), 2) AS denied_outstanding
FROM healthcare_claims_vscode
WHERE claim_status = 'Denied'
GROUP BY insurance_type
ORDER BY denied_claims DESC;