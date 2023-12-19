terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.9.0"
    }
  }
}

provider "google" {
  project = "dtc-de-project1"
  region  = "us-central1"
}

resource "google_storage_bucket" "etl_project1_bucket1" {
  name          = "dtc-de-project1-terra-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "etl_project1_bq_dataset" {
  dataset_id = "project1_bq_dataset1"
}