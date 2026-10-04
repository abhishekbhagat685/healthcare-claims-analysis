USE healthcare_claims_db;

-- KPI 1: Overall Healthcare Claims Summary
-- Purpose: Summarize claim volume and financial amounts.

SELECT
    COUNT(*) AS total_claims,
    COUNT(DISTINCT claim_id) AS unique_claims,

    ROUND(SUM(billed_amount), 2) AS total_billed_amount,
    ROUND(SUM(allowed_amount), 2) AS total_allowed_amount,
    ROUND(SUM(paid_amount), 2) AS total_paid_amount,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding_amount

FROM healthcare_claims_vscode;