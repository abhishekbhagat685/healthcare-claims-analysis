USE healthcare_claims_db;

-- KPI 4: Denial Analysis
-- Purpose: Analyze denied claims, denial reasons, and insurance patterns.

-- Part A: Overall denial metrics
SELECT
    COUNT(*) AS total_claims,
    SUM(CASE
        WHEN claim_status = 'Denied' THEN 1
        ELSE 0
    END) AS denied_claims,
    ROUND(
        100.0 * SUM(CASE
            WHEN claim_status = 'Denied' THEN 1
            ELSE 0
        END) / NULLIF(COUNT(*), 0),
        2
    ) AS denial_percentage,
    ROUND(
        SUM(CASE
            WHEN claim_status = 'Denied' THEN outstanding_amount
            ELSE 0
        END),
        2
    ) AS denied_claims_outstanding
FROM healthcare_claims_vscode;


-- Part B: Denial reasons
SELECT
    reason_code,
    COUNT(*) AS denied_claim_count,
    ROUND(
        100.0 * COUNT(*) /
        NULLIF(
            (SELECT COUNT(*)
             FROM healthcare_claims_vscode
             WHERE claim_status = 'Denied'),
            0
        ),
        2
    ) AS percentage_of_denied_claims
FROM healthcare_claims_vscode
WHERE claim_status = 'Denied'
  AND reason_code IS NOT NULL
  AND TRIM(reason_code) <> ''
GROUP BY reason_code
ORDER BY denied_claim_count DESC;


-- Part C: Denials by insurance type
SELECT
    insurance_type,
    COUNT(*) AS denied_claim_count,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding
FROM healthcare_claims_vscode
WHERE claim_status = 'Denied'
GROUP BY insurance_type
ORDER BY denied_claim_count DESC;