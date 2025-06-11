# variables.tf
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "domain_name" {
  description = "Your custom domain (e.g., example.com)"
  type        = string
}

variable "bucket_name" {
  description = "Name of your storage bucket"
  type        = string
  default     = "trendsleuth-website"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}
