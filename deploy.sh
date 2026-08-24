#!/bin/bash
set -e

SERVICE_NAME="yahoo-fantasy-mcp"
REGION="us-east1"

echo "Deploying ${SERVICE_NAME} to Google Cloud Run (scale-to-zero)..."

gcloud run deploy ${SERVICE_NAME} \
  --source . \
  --platform managed \
  --region ${REGION} \
  --min-instances 0 \
  --max-instances 1 \
  --allow-unauthenticated \
  --set-env-vars YAHOO_SECRET_NAME="YAHOO_OAUTH_TOKEN"

echo "Deployment complete! Copy the SSE endpoint URL provided above into your Gemini / Agent settings."
