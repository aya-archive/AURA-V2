#!/bin/bash
# A.U.R.A AWS Deployment Script
# This script deploys the AURA platform to AWS using ECS and RDS

set -e

# Configuration
AWS_REGION="us-east-1"
ECS_CLUSTER="aura-cluster"
ECS_SERVICE="aura-service"
RDS_INSTANCE="aura-db"
S3_BUCKET="aura-data-bucket"

echo "🚀 Starting AURA deployment to AWS..."

# 1. Create ECS Cluster
echo "📦 Creating ECS cluster..."
aws ecs create-cluster --cluster-name $ECS_CLUSTER --region $AWS_REGION

# 2. Create RDS PostgreSQL instance
echo "🗄️ Creating RDS database..."
aws rds create-db-instance \
    --db-instance-identifier $RDS_INSTANCE \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username aura_admin \
    --master-user-password $(openssl rand -base64 32) \
    --allocated-storage 20 \
    --region $AWS_REGION

# 3. Create S3 bucket for data storage
echo "📁 Creating S3 bucket for data..."
aws s3 mb s3://$S3_BUCKET --region $AWS_REGION

# 4. Build and push Docker image to ECR
echo "🐳 Building and pushing Docker image..."
aws ecr create-repository --repository-name aura-platform --region $AWS_REGION || true
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

docker build -t aura-platform .
docker tag aura-platform:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aura-platform:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aura-platform:latest

# 5. Create ECS task definition
echo "⚙️ Creating ECS task definition..."
cat > task-definition.json << EOF
{
  "family": "aura-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::$AWS_ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "aura-container",
      "image": "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/aura-platform:latest",
      "portMappings": [
        {
          "containerPort": 7860,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "GRADIO_SERVER_PORT",
          "value": "7860"
        },
        {
          "name": "GRADIO_SERVER_ADDRESS",
          "value": "0.0.0.0"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/aura",
          "awslogs-region": "$AWS_REGION",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF

aws ecs register-task-definition --cli-input-json file://task-definition.json --region $AWS_REGION

# 6. Create ECS service
echo "🎯 Creating ECS service..."
aws ecs create-service \
    --cluster $ECS_CLUSTER \
    --service-name $ECS_SERVICE \
    --task-definition aura-task \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}" \
    --region $AWS_REGION

echo "✅ AURA deployment completed!"
echo "🌐 Your application will be available at the ECS service endpoint"
echo "📊 Monitor your deployment in the AWS Console"
