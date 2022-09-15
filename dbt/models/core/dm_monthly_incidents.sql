
{{ config(materialized='table') }}

WITH incident_data AS (
    SELECT * FROM {{ ref('fact_incidents') }}
)

SELECT
    incident_year,
    FORMAT_DATE("%m", DATE_TRUNC(incident_date, MONTH)) AS incident_month,
    incident_category,

    COUNT(incident_id) AS incident_count,
FROM
    incident_data
GROUP BY 1,2,3
ORDER BY 1,2