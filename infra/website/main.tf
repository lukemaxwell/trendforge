terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Create the storage bucket
resource "google_storage_bucket" "static_site" {
  name          = var.bucket_name
  location      = "US"
  force_destroy = true

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  # Enable uniform bucket-level access
  uniform_bucket_level_access = true

  # Enable versioning (optional)
  versioning {
    enabled = true
  }

  # CORS configuration for web access
  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# Make bucket publicly readable
resource "google_storage_bucket_iam_member" "public_read" {
  bucket = google_storage_bucket.static_site.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

# Upload index.html
resource "google_storage_bucket_object" "index_html" {
  name   = "index.html"
  bucket = google_storage_bucket.static_site.name
  source = "index.html"
  
  # Content type
  content_type = "text/html"
  
  # Cache control
  cache_control = "public, max-age=3600"
}

# Upload 404.html (optional)
resource "google_storage_bucket_object" "error_html" {
  name   = "404.html"
  bucket = google_storage_bucket.static_site.name
  source = "404.html"
  
  content_type  = "text/html"
  cache_control = "public, max-age=3600"
  
  # Only create if 404.html exists
  count = fileexists("404.html") ? 1 : 0
}

# Upload all files from a directory (optional)
resource "google_storage_bucket_object" "static_files" {
  for_each = fileset("${path.module}/static", "**/*")
  
  name   = each.value
  bucket = google_storage_bucket.static_site.name
  source = "${path.module}/static/${each.value}"
  
  # Determine content type based on file extension
  content_type = lookup({
    "html" = "text/html",
    "css"  = "text/css",
    "js"   = "application/javascript",
    "json" = "application/json",
    "png"  = "image/png",
    "jpg"  = "image/jpeg",
    "jpeg" = "image/jpeg",
    "gif"  = "image/gif",
    "svg"  = "image/svg+xml",
    "ico"  = "image/x-icon",
    "pdf"  = "application/pdf"
  }, split(".", each.value)[length(split(".", each.value)) - 1], "application/octet-stream")
  
  cache_control = "public, max-age=3600"
}
resource "google_compute_global_address" "default" {
  name = "static-site-ip"
}

# Create managed SSL certificate
resource "google_compute_managed_ssl_certificate" "default" {
  name = "static-site-ssl-cert"

  managed {
    domains = [var.domain_name]
  }
}

# Reserve a static IP address
# Backend bucket for static site

resource "google_compute_backend_bucket" "static_site" {
  name        = "static-site-backend"
  bucket_name = google_storage_bucket.static_site.name
  enable_cdn  = true
}
resource "google_compute_url_map" "https" {
  name            = "static-site-https-url-map"
  default_service = google_compute_backend_bucket.static_site.id

  host_rule {
    hosts        = [var.domain_name]
    path_matcher = "allpaths"
  }

  path_matcher {
    name            = "allpaths"
    default_service = google_compute_backend_bucket.static_site.id
  }
}

# URL map for HTTP to HTTPS redirect
resource "google_compute_url_map" "http_redirect" {
  name = "static-site-http-redirect"

  default_url_redirect {
    https_redirect         = true
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
  }
}

# HTTPS target proxy
resource "google_compute_target_https_proxy" "default" {
  name             = "static-site-https-proxy"
  url_map          = google_compute_url_map.https.id
  ssl_certificates = [google_compute_managed_ssl_certificate.default.id]
}

# HTTP target proxy for redirect
resource "google_compute_target_http_proxy" "default" {
  name    = "static-site-http-proxy"
  url_map = google_compute_url_map.http_redirect.id
}

# Global forwarding rule for HTTPS
resource "google_compute_global_forwarding_rule" "https" {
  name       = "static-site-https-forwarding-rule"
  target     = google_compute_target_https_proxy.default.id
  port_range = "443"
  ip_address = google_compute_global_address.default.address
}

# Global forwarding rule for HTTP redirect
resource "google_compute_global_forwarding_rule" "http" {
  name       = "static-site-http-forwarding-rule"
  target     = google_compute_target_http_proxy.default.id
  port_range = "80"
  ip_address = google_compute_global_address.default.address
}

