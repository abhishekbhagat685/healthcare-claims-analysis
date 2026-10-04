USE healthcare_claims_db;

-- KPI 7: Follow-up Analysis
-- Purpose: Analyze follow-up requirements and outstanding balances.

-- Part A: Follow-up summary
SELECT
    follow_up_required,
    COUNT(*) AS total_claims,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding,
    ROUND(AVG(outstanding_amount), 2) AS average_outstanding
FROM healthcare_claims_vscode
GROUP BY follow_up_required
ORDER BY total_outstanding DESC;


-- Part B: Follow-up by claim status
SELECT
    claim_status,
    follow_up_required,
    COUNT(*) AS total_claims,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding,
    ROUND(AVG(outstanding_amount), 2) AS average_outstanding
FROM healthcare_claims_vscode
GROUP BY
    claim_status,
    follow_up_required
ORDER BY total_outstanding DESC;


-- Part C: Follow-up flags among denied claims
SELECT
    follow_up_required,
    COUNT(*) AS denied_claims,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding
FROM healthcare_claims_vscode
WHERE claim_status = 'Denied'
GROUP BY follow_up_required
ORDER BY denied_claims DESC;