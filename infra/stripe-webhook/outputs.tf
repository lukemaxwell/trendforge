output "stripe_webhook_url" {
  value = google_cloud_run_v2_service.stripe_webhook.uri
}
