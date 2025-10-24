#!/bin/bash
# A.U.R.A Google Cloud Platform Deployment Script
# This script deploys the AURA platform to GCP using Cloud Run and Cloud SQL

set -e

# Configuration
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
SERVICE_NAME="aura-platform"
DB_INSTANCE="aura-db"

echo "🚀 Starting AURA deployment to Google Cloud Platform..."

# 1. Set project
echo "🎯 Setting GCP project..."
gcloud config set project $PROJECT_ID

# 2. Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable storage.googleapis.com

# 3. Create Cloud SQL PostgreSQL instance
echo "🗄️ Creating Cloud SQL database..."
gcloud sql instances create $DB_INSTANCE \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=$REGION \
    --storage-type=SSD \
    --storage-size=10GB \
    --storage-auto-increase

# 4. Create database
echo "📊 Creating database..."
gcloud sql databases create aura_db --instance=$DB_INSTANCE

# 5. Create user
echo "👤 Creating database user..."
gcloud sql users create aura_user \
    --instance=$DB_INSTANCE \
    --password=$(openssl rand -base64 32)

# 6. Build and deploy to Cloud Run
echo "🐳 Building and deploying to Cloud Run..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/aura-platform

# 7. Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/aura-platform \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 7860 \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 10 \
    --set-env-vars "GRADIO_SERVER_PORT=7860,GRADIO_SERVER_ADDRESS=0.0.0.0"

# 8. Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo "✅ AURA deployment completed!"
echo "🌐 Your application is available at: $SERVICE_URL"
echo "📊 Monitor your deployment in the GCP Console"
