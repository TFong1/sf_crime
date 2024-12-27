# Load SF Incident Data to External Staging Tables

The Airflow DAG has uploaded the parquet files to Google Storage bucket. Now, we need to insert the data in the parquet files to our BigQuery database. The data will be uploaded to a BigQuery staging table where dbt will transform the data to a data warehouse.

Follow the procedure to upload the data to the staging table:

1. Launch a web browser
2. Navigate to the [Google Cloud Console website](https://console.cloud.google.com)
3. Select the [project](../gcp/README.md#create-a-google-cloud-project) you created
4. Click on the "Run a query in BigQuery" link
    * Alternatively, you can click on the "hamburger" menu at the top left corner and select "BigQuery"
5. Open the load-parquet-to-staging.sql file in BigQuery query editor or copy and paste the contents of the file and paste it on the query editor
6. Replace the "external_incident_data" with the full BigQuery path to the database
7. Execute the load-parquet-to-staging.sql script on Google Cloud Platform to load all of the data in parquet files to an external BigQuery table

The external_incident_data BigQuery table will be used as the basis of the data warehouse.  dbt will transform this data into it's final data warehouse format.

## Next Step

Go to [dbt](../dbt/) to transform the incident data.
