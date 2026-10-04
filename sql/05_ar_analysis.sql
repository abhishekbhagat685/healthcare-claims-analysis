USE healthcare_claims_db;

-- KPI 5: Accounts Receivable (A/R) Analysis
-- Purpose: Analyze outstanding balances by A/R status.

-- Part A: A/R summary by status
SELECT
    ar_status,
    COUNT(*) AS total_claims,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding,
    ROUND(AVG(outstanding_amount), 2) AS average_outstanding
FROM healthcare_claims_vscode
GROUP BY ar_status
ORDER BY total_outstanding DESC;


-- Part B: A/R status by claim status
SELECT
    ar_status,
    claim_status,
    COUNT(*) AS total_claims,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding
FROM healthcare_claims_vscode
GROUP BY
    ar_status,
    claim_status
ORDER BY total_outstanding DESC;


-- Part C: Claims flagged for follow-up by A/R status
SELECT
    ar_status,
    follow_up_required,
    COUNT(*) AS total_claims,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding
FROM healthcare_claims_vscode
GROUP BY
    ar_status,
    follow_up_required
ORDER BY total_outstanding DESC;