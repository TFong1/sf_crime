
{{ config(materialized='view') }}

WITH incident_data AS (
    SELECT
        *
    FROM {{ source('staging', 'external_incident_data') }}
)
SELECT
    row_id,
    CAST(incident_datetime AS DATETIME) AS incident_datetime,
    CAST(incident_date AS DATE) AS incident_date,
    CAST(incident_time AS TIME) AS incident_time, -- TIMESTAMP?
    incident_year,
    TRIM(incident_day_of_week) AS incident_day_of_week,
    incident_id,
    incident_number,
    incident_code,
    NULLIF(TRIM(incident_category), '') AS incident_category,
    NULLIF(TRIM(incident_subcategory), '') AS incident_subcategory,
    TRIM(incident_description) AS incident_description,
    CAST(report_datetime AS DATETIME) AS report_datetime,
    TRIM(report_type_code) AS report_type_code,
    TRIM(report_type_description) AS report_type_description,
    TRIM(resolution) AS resolution,
    CAST(cad_number AS INTEGER) AS cad_number,
    NULLIF(TRIM(intersection), '') AS intersection,
    CAST(cnn AS INTEGER) AS CNN,
    TRIM(police_district) AS police_district,
    NULLIF(TRIM(analysis_neighborhood), '') AS analysis_neighborhood,
    CAST(supervisor_district AS INTEGER) AS supervisor_district,
    latitude,
    longitude,
    --CAST(point AS GEOGRAPHY) AS point,
    CAST (
        CASE
            WHEN filed_online = 1.0 THEN TRUE
            ELSE FALSE
        END
        AS BOOLEAN
    ) AS filed_online
FROM incident_data

-- Use command below to not run in test mode
-- dbt build --m <model.sql> --var 'is_test_run: false' 
{% if var('is_test_run', default=true) %}

    LIMIT 100

{% endif %}
