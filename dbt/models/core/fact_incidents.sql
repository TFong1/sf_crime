
{{ config(
    materialized='table',
    partition_by={
        "field": "incident_datetime",
        "data_type": "datetime",
        "granularity": "month"
    }
) }}


WITH incident_data AS (
    SELECT * FROM {{ ref('staging_incident_data') }}
),

dim_incident_codes AS (
    SELECT * FROM {{ ref('dim_incident_codes') }}
)

SELECT
    incident_data.row_id,
    incident_data.incident_datetime,
    incident_data.incident_date,
    incident_data.incident_time,
    incident_data.incident_year,
    incident_data.incident_day_of_week,
    incident_data.incident_id,
    incident_data.incident_number,
    incident_data.incident_code,
    dim_incident_codes.category AS incident_category,
    dim_incident_codes.subcategory AS incident_subcategory,
    incident_data.incident_description,
    incident_data.report_datetime,
    incident_data.report_type_code,
    incident_data.report_type_description,
    incident_data.resolution,
    incident_data.cad_number,
    incident_data.intersection,
    incident_data.CNN,
    incident_data.police_district,
    incident_data.analysis_neighborhood,
    incident_data.supervisor_district,
    incident_data.latitude,
    incident_data.longitude,
    incident_data.point,
    incident_data.filed_online
FROM incident_data
INNER JOIN dim_incident_codes
    ON incident_data.incident_code = dim_incident_codes.incident_code
