
{{ config(materialized='table') }}

SELECT
    inc_code AS incident_code,
    category,
    subcategory
FROM
    {{ ref('incident_codes_lookup') }}
WHERE
    category IS NOT NULL AND subcategory IS NOT NULL
