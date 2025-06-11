terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.39.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_domain_mapping" "streamlit_domain" {
  name     = "app.trendsleuth.ai"
  location = var.region

  metadata {
    namespace = var.project_id
  }

  spec {
    route_name = var.streamlit_service_name
  }
}
