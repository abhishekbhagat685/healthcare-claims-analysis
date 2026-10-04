USE healthcare_claims_db;

-- KPI 2: Claim Status Analysis
-- Purpose: Analyze claim counts and outstanding amounts by status.

SELECT
    claim_status,
    COUNT(*) AS total_claims,

    ROUND(
        100.0 * COUNT(*) /
        NULLIF((SELECT COUNT(*) FROM healthcare_claims_vscode), 0),
        2
    ) AS percentage_of_claims,

    ROUND(SUM(billed_amount), 2) AS total_billed_amount,
    ROUND(SUM(paid_amount), 2) AS total_paid_amount,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding_amount

FROM healthcare_claims_vscode
GROUP BY claim_status
ORDER BY total_claims DESC;