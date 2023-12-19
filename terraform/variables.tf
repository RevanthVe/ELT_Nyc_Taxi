variable "credentials" {
    description = "cloud credentials"
    default = "/Users/revanthvemula/ETL_Project1/keys/gcp-creds.json"
}

variable "project" {
    description = "project name"
    default = "dtc-de-project1"
}

variable "region" {
    description = "region name"
    default = "us-central1"
}

variable "gcs_storage_class" {
    description = "bucket storage class"
    default = "STANDARD"
}

variable "location" {
    description = "location name"
    default = "US"
}

variable "gcs_bucket_name" {
    description = "gcs bucket name"
    default = "dtc-de-project1-terra-bucket"
}

variable "bq_dataset_name" {
    description = "bq dataset name"
    default = "project1_bq_dataset1"
}