
locals {
  data_lake_bucket = "sf-crime-data-lake"
}

variable "project" {
    type = string
    description = "Enter the Project ID for the Google Cloud Service:"
}

variable "region" {
    type = string
    description = "Region for GCP resources. Choose as per your location:  https://cloud.google.com/about/locations"
    default = "us-west2"
}

variable "storage_class" {
    type = string
    description = "Storage class type for your bucket. Check official docs for more info."
    default = "STANDARD"
}

variable "BQ_DATASET" {
    type = string
    description = "BigQuery Dataset that raw data (from GCS) will be written to."
    default = "sf_crime_data_all"
}

variable "credentials" {
  type = string
  description = "Location of Google credentials file"
  default = "/home/fongt/.google/credentials/etl-sf-crime-76032-credentials.json"
}