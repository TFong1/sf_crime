# Load SF Incident Data to External Staging Tables

Execute the load-parquet-to-staging.sql script on Google Cloud Platform to load all of the data in parquet files to an external BigQuery table.

Replace the "external_incident_data" with the full BigQuery path to the database.

The external_incident_data BigQuery table will be used as the basis of the data warehouse.  dbt will transform this data into it's final data warehouse format.
