output "load_balancer_ip" {
  description = "IP address of the load balancer"
  value       = google_compute_global_address.default.address
}

output "ssl_certificate_name" {
  description = "Name of the SSL certificate (check status in GCP Console)"
  value       = google_compute_managed_ssl_certificate.default.name
}

output "ssl_certificate_check_command" {
  description = "Command to check SSL certificate status"
  value       = "gcloud compute ssl-certificates describe ${google_compute_managed_ssl_certificate.default.name} --global --format='value(managed.status)'"
}

# URL map for HTTPS

output "bucket_name" {
  description = "Name of the storage bucket"
  value       = google_storage_bucket.static_site.name
}

output "bucket_url" {
  description = "Direct bucket URL"
  value       = "https://storage.googleapis.com/${google_storage_bucket.static_site.name}/index.html"
}

output "dns_instructions" {
  description = "DNS configuration instructions"
  value = <<-EOT
    Configure your DNS to point to the load balancer:
    
    A record: ${var.domain_name} -> ${google_compute_global_address.default.address}
    
    If using a subdomain like www.${var.domain_name}, create:
    CNAME record: www -> ${var.domain_name}
  EOT
}
