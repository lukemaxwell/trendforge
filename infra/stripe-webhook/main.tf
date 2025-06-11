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

# Service account for webhook
resource "google_service_account" "webhook_sa" {
  account_id   = "trendsleuth-stripe-webhook-sa"
  display_name = "Trendsleuth Stripe Webhook Service Account"
}

# Firestore access for webhook
resource "google_project_iam_member" "webhook_firestore_access" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.webhook_sa.email}"
}

# Secret Manager access for webhook
resource "google_project_iam_member" "webhook_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.webhook_sa.email}"
}

# Stripe Secret
resource "google_secret_manager_secret" "stripe_secret" {
  secret_id = "stripe-api-key"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "stripe_secret_version" {
  secret      = google_secret_manager_secret.stripe_secret.id
  secret_data = var.stripe_secret_value
}

# Stripe Webhook Signing Secret
resource "google_secret_manager_secret" "stripe_endpoint_secret" {
  secret_id = "stripe-endpoint-secret"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "stripe_endpoint_secret_version" {
  secret      = google_secret_manager_secret.stripe_endpoint_secret.id
  secret_data = var.stripe_endpoint_secret_value
}

# Cloud Run v2 Service for Stripe Webhook
resource "google_cloud_run_v2_service" "stripe_webhook" {
  name     = "trendsleuth-stripe-webhook"
  location = var.region

  template {
    service_account = google_service_account.webhook_sa.email

    containers {
      image = var.fastapi_image

      env {
        name  = "STRIPE_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.stripe_secret.id
            version = "latest"
          }
        }
      }

      env {
        name  = "STRIPE_ENDPOINT_SECRET"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.stripe_endpoint_secret.id
            version = "latest"
          }
        }
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}
