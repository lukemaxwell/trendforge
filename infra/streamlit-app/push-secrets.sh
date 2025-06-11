#!/bin/bash

VARS_FILE="secrets.auto.tfvars"

echo "🚀 Starting secrets upload from $VARS_FILE"

# List of var name → secret name mappings
#firebase_project_id_value=firebase-project-id
#firebase_private_key_id_value=firebase-private-key-id
#firebase_private_key_value=firebase-private-key
#firebase_client_email_value=firebase-client-email
#firebase_client_id_value=firebase-client-id
#firebase_client_cert_url_value=firebase-client-cert-url
MAPPINGS="
openai_api_key_value=openai-api-key
stripe_api_key_value=stripe-api-key
reddit_client_id_value=reddit-client-id
reddit_client_secret_value=reddit-client-secret
reddit_user_agent_value=reddit-user-agent
"

# Process each mapping
while IFS='=' read -r VAR_NAME SECRET_NAME; do

    # Skip empty lines
    [[ -z "$VAR_NAME" ]] && continue

    VALUE=$(grep "^$VAR_NAME" "$VARS_FILE" | sed -E 's/^.*=\s*"([^"]+)"$/\1/')

    if [[ -z "$VALUE" ]]; then
        echo "⚠️  Warning: No value found for $VAR_NAME → skipping $SECRET_NAME"
        continue
    fi

    echo "🔑 Pushing secret: $SECRET_NAME"

    echo -n "$VALUE" | gcloud secrets versions add "$SECRET_NAME" --data-file=-

done <<< "$MAPPINGS"

echo "✅ All secrets pushed."
