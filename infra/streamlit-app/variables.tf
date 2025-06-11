variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
}

variable "streamlit_image" {
  description = "Streamlit container image"
  type        = string
}

# Secret values — provided via secrets.auto.tfvars

variable "openai_api_key_value" {
  description = "OpenAI API Key"
  type        = string
}

variable "stripe_api_key_value" {
  description = "Stripe API Key"
  type        = string
}

variable "reddit_client_id_value" {
  description = "Reddit Client ID"
  type        = string
}

variable "reddit_client_secret_value" {
  description = "Reddit Client Secret"
  type        = string
}

variable "reddit_user_agent_value" {
  description = "Reddit User Agent"
  type        = string
}

variable "firebase_project_id_value" {
  description = "Firebase Project ID"
  type        = string
}

variable "firebase_private_key_id_value" {
  description = "Firebase Private Key ID"
  type        = string
}

variable "firebase_private_key_value" {
  description = "Firebase Private Key"
  type        = string
}

variable "firebase_client_email_value" {
  description = "Firebase Client Email"
  type        = string
}

variable "firebase_client_id_value" {
  description = "Firebase Client ID"
  type        = string
}

variable "firebase_client_cert_url_value" {
  description = "Firebase Client Certificate URL"
  type        = string
}
