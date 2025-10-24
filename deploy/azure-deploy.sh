#!/bin/bash
# A.U.R.A Azure Deployment Script
# This script deploys the AURA platform to Azure using Container Instances and Azure Database

set -e

# Configuration
RESOURCE_GROUP="aura-rg"
LOCATION="eastus"
CONTAINER_NAME="aura-platform"
DB_SERVER="aura-db-server"

echo "🚀 Starting AURA deployment to Microsoft Azure..."

# 1. Create resource group
echo "📦 Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# 2. Create Azure Database for PostgreSQL
echo "🗄️ Creating Azure Database for PostgreSQL..."
az postgres flexible-server create \
    --resource-group $RESOURCE_GROUP \
    --name $DB_SERVER \
    --location $LOCATION \
    --admin-user aura_admin \
    --admin-password $(openssl rand -base64 32) \
    --sku-name Standard_B1ms \
    --tier Burstable \
    --public-access 0.0.0.0 \
    --storage-size 32

# 3. Create database
echo "📊 Creating database..."
az postgres flexible-server db create \
    --resource-group $RESOURCE_GROUP \
    --server-name $DB_SERVER \
    --database-name aura_db

# 4. Create Azure Container Registry
echo "🐳 Creating Azure Container Registry..."
az acr create \
    --resource-group $RESOURCE_GROUP \
    --name auraacr \
    --sku Basic \
    --admin-enabled true

# 5. Build and push image
echo "🔨 Building and pushing Docker image..."
az acr build --registry auraacr --image aura-platform:latest .

# 6. Create container instance
echo "🚀 Creating Azure Container Instance..."
az container create \
    --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_NAME \
    --image auraacr.azurecr.io/aura-platform:latest \
    --cpu 2 \
    --memory 4 \
    --ports 7860 \
    --environment-variables \
        GRADIO_SERVER_PORT=7860 \
        GRADIO_SERVER_ADDRESS=0.0.0.0 \
    --registry-login-server auraacr.azurecr.io \
    --registry-username $(az acr credential show --name auraacr --query username --output tsv) \
    --registry-password $(az acr credential show --name auraacr --query passwords[0].value --output tsv)

# 7. Get public IP
echo "🌐 Getting public IP address..."
PUBLIC_IP=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query ipAddress.ip --output tsv)

echo "✅ AURA deployment completed!"
echo "🌐 Your application is available at: http://$PUBLIC_IP:7860"
echo "📊 Monitor your deployment in the Azure Portal"
