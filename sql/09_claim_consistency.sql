USE healthcare_claims_db;

-- KPI 9: Claim Consistency Analysis
-- Purpose: Compare recorded claim status with claim outcome.
-- Note: Differences may be valid business states, not necessarily errors.

-- Part A: Claim status and outcome cross-tabulation
SELECT
    claim_status,
    outcome,
    COUNT(*) AS total_claims
FROM healthcare_claims_vscode
GROUP BY
    claim_status,
    outcome
ORDER BY
    claim_status,
    outcome;


-- Part B: Overall outcome distribution
SELECT
    outcome,
    COUNT(*) AS total_claims,
    ROUND(
        100.0 * COUNT(*) /
        NULLIF((SELECT COUNT(*) FROM healthcare_claims_vscode), 0),
        2
    ) AS percentage_of_claims
FROM healthcare_claims_vscode
GROUP BY outcome
ORDER BY total_claims DESC;


-- Part C: Missing or blank status/outcome values
SELECT
    SUM(
        CASE
            WHEN claim_status IS NULL
                 OR TRIM(claim_status) = ''
            THEN 1 ELSE 0
        END
    ) AS missing_claim_status,

    SUM(
        CASE
            WHEN outcome IS NULL
                 OR TRIM(outcome) = ''
            THEN 1 ELSE 0
        END
    ) AS missing_outcome

FROM healthcare_claims_vscode;