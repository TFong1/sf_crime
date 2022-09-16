CREATE OR REPLACE EXTERNAL TABLE  `external_incident_data`
OPTIONS (
  format = "PARQUET",
  uris = ["gs://sf-crime-data-lake/raw/sf_crime_data/2020/sf_crime_2020-*.parquet",
          "gs://sf-crime-data-lake/raw/sf_crime_data/2021/sf_crime_2021-*.parquet",
          "gs://sf-crime-data-lake/raw/sf_crime_data/2022/sf_crime_2022-*.parquet"]
)
