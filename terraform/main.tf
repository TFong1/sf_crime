terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for Google) or "s3" (for AWS), if you would like to preserve your tf-state online
  required_providers {
    google = {
        source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region = var.region
  credentials = file(var.credentials)  # Use this if you don't want to use environmental variable GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
# Reference:  https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "sf-crime-data-lake" {
  name = "${local.data_lake_bucket}_${var.project}"  # concatenating data lake bucket & project name for unique naming
  location = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
        type = "Delete"
    }
    condition {
        age = 30   // Delete after 30 days
    }
  }

  force_destroy = true
}

# Data Warehouse
# Reference:  https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}