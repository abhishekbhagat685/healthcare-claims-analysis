USE healthcare_claims_db;

-- KPI 10: Financial Reconciliation
-- Purpose: Validate outstanding amounts against the defined formula.
-- Assumption: Outstanding = Allowed Amount - Paid Amount.

SELECT
    COUNT(*) AS total_claims,

    ROUND(SUM(billed_amount), 2) AS total_billed,
    ROUND(SUM(allowed_amount), 2) AS total_allowed,
    ROUND(SUM(paid_amount), 2) AS total_paid,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding,

    ROUND(
        SUM(allowed_amount - paid_amount),
        2
    ) AS calculated_outstanding,

    ROUND(
        SUM(
            outstanding_amount -
            (allowed_amount - paid_amount)
        ),
        2
    ) AS reconciliation_difference

FROM healthcare_claims_vscode;