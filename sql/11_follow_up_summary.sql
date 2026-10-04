
USE healthcare_claims_db;

-- KPI 11: Follow-Up Summary
-- Purpose: Analyze follow-up requirements by claim status.
-- Table: healthcare_claims_vscode

-- Query 1: Overall follow-up summary
SELECT
    follow_up_required,
    COUNT(*) AS total_claims,
    ROUND(
        100.0 * COUNT(*) /
        NULLIF((SELECT COUNT(*) FROM healthcare_claims_vscode), 0),
        2
    ) AS percentage_of_claims,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding,
    ROUND(AVG(outstanding_amount), 2) AS average_outstanding
FROM healthcare_claims_vscode
GROUP BY follow_up_required
ORDER BY total_outstanding DESC;

-- Query 2: Follow-up breakdown by claim status
SELECT
    claim_status,
    follow_up_required,
    COUNT(*) AS total_claims,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding,
    ROUND(AVG(outstanding_amount), 2) AS average_outstanding
FROM healthcare_claims_vscode
GROUP BY claim_status, follow_up_required
ORDER BY total_outstanding DESC;

-- Query 3: Denied claims by follow-up requirement
SELECT
    follow_up_required,
    COUNT(*) AS denied_claims,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding
FROM healthcare_claims_vscode
WHERE claim_status = 'Denied'
GROUP BY follow_up_required
ORDER BY denied_claims DESC;