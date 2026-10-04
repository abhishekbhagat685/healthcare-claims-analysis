USE healthcare_claims_db;

-- KPI 8: Claim Aging Analysis
-- Purpose: Group claims by days since date of service.
-- Note: This is not true A/R aging because the claim submission
-- or A/R entry date is not available in the dataset.

SELECT
    CASE
        WHEN DATEDIFF(CURDATE(), date_of_service) <= 30
            THEN '0-30 Days'
        WHEN DATEDIFF(CURDATE(), date_of_service) <= 60
            THEN '31-60 Days'
        WHEN DATEDIFF(CURDATE(), date_of_service) <= 90
            THEN '61-90 Days'
        ELSE '90+ Days'
    END AS claim_age_bucket,

    COUNT(*) AS total_claims,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding,
    ROUND(AVG(outstanding_amount), 2) AS average_outstanding

FROM healthcare_claims_vscode
WHERE date_of_service IS NOT NULL
  AND date_of_service <= CURDATE()

GROUP BY claim_age_bucket

ORDER BY
    CASE claim_age_bucket
        WHEN '0-30 Days' THEN 1
        WHEN '31-60 Days' THEN 2
        WHEN '61-90 Days' THEN 3
        ELSE 4
    END;