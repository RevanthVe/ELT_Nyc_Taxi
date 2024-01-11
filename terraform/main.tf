terraform {
  required_providers {
    google = {
        credentials = file(var.credentials)
      source  = "hashicorp/google"
      version = "5.9.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

resource "google_storage_bucket" "etl_project1_bucket1" {
  name          = var.gcs_bucket_name
  location      = var.location
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
  dataset_id = var.bq_dataset_name
}