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

# Streamlit Cloud Run V2 Service
resource "google_cloud_run_v2_service" "streamlit_app" {
  name     = "trendsleuth-streamlit"
  location = var.region

  template {
    containers {
      image = var.streamlit_image

      ports {
        container_port = 8080
      }

      env {
        name  = "OPENAI_API_KEY"
        value = var.openai_api_key_value
      }

      env {
        name  = "STRIPE_API_KEY"
        value = var.stripe_api_key_value
      }

      env {
        name  = "REDDIT_CLIENT_ID"
        value = var.reddit_client_id_value
      }

      env {
        name  = "REDDIT_CLIENT_SECRET"
        value = var.reddit_client_secret_value
      }

      env {
        name  = "REDDIT_USER_AGENT"
        value = var.reddit_user_agent_value
      }

      env {
        name  = "FIREBASE_PROJECT_ID"
        value = var.firebase_project_id_value
      }

      env {
        name  = "FIREBASE_PRIVATE_KEY_ID"
        value = var.firebase_private_key_id_value
      }

      env {
        name  = "FIREBASE_PRIVATE_KEY"
        value = var.firebase_private_key_value
      }

      env {
        name  = "FIREBASE_CLIENT_EMAIL"
        value = var.firebase_client_email_value
      }

      env {
        name  = "FIREBASE_CLIENT_ID"
        value = var.firebase_client_id_value
      }

      env {
        name  = "FIREBASE_CLIENT_CERT_URL"
        value = var.firebase_client_cert_url_value
      }
    }
  }
}

# Secret resources — safe pattern → no versions → push values via push_secrets.sh

resource "google_secret_manager_secret" "openai_api_key" {
  secret_id = "openai-api-key"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "stripe_api_key" {
  secret_id = "stripe-api-key"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "reddit_client_id" {
  secret_id = "reddit-client-id"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "reddit_client_secret" {
  secret_id = "reddit-client-secret"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "reddit_user_agent" {
  secret_id = "reddit-user-agent"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "firebase_project_id" {
  secret_id = "firebase-project-id"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "firebase_private_key_id" {
  secret_id = "firebase-private-key-id"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "firebase_private_key" {
  secret_id = "firebase-private-key"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "firebase_client_email" {
  secret_id = "firebase-client-email"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "firebase_client_id" {
  secret_id = "firebase-client-id"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "firebase_client_cert_url" {
  secret_id = "firebase-client-cert-url"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}
