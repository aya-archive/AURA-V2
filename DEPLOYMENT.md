# 🚀 AURA-V2 Deployment Guide

**Complete deployment guide for the Adaptive User Retention Assistant platform**

## 📋 Quick Start Options

### 🏃‍♂️ **Fastest: Local Development**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample data
python generate_mock_data.py

# 3. Run data pipeline
python -c "from src.data_pipeline.orchestrator import DataPipelineOrchestrator; orchestrator = DataPipelineOrchestrator(); orchestrator.run_complete_pipeline()"

# 4. Launch application
python aura_gradio_app.py
```
**Access:** http://localhost:7860

---

### 🐳 **Recommended: Docker Deployment**
```bash
# Quick start with Docker Compose
docker-compose up -d

# Production deployment
docker-compose -f docker-compose.yml up -d
```
**Access:** http://localhost:7860

---

### ☁️ **Cloud Deployment Options**

#### A. **Gradio Spaces (Easiest)**
1. Push code to GitHub
2. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
3. Create new Gradio space
4. Connect GitHub repository
5. Deploy automatically!

#### B. **Streamlit Cloud**
1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Connect GitHub repository
3. Configure environment variables
4. Deploy with one click

#### C. **AWS Deployment**
```bash
# Make script executable and run
chmod +x deploy/aws-deploy.sh
./deploy/aws-deploy.sh
```

#### D. **Google Cloud Platform**
```bash
# Make script executable and run
chmod +x deploy/gcp-deploy.sh
./deploy/gcp-deploy.sh
```

#### E. **Microsoft Azure**
```bash
# Make script executable and run
chmod +x deploy/azure-deploy.sh
./deploy/azure-deploy.sh
```

---

## 🏗️ Architecture Overview

Your AURA-V2 platform uses a **Medallion Architecture** with three data layers:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Bronze Layer  │───▶│   Silver Layer  │───▶│    Gold Layer   │
│                 │    │                 │    │                 │
│ • Raw Data      │    │ • Cleaned Data  │    │ • Analytics     │
│ • CSV Files     │    │ • Enriched Data │    │ • KPIs          │
│ • Logs          │    │ • Derived Metrics│   │ • Insights      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🧠 AI Models Included
- **Prophet Forecasting**: Time series prediction for revenue and engagement
- **Rule-based Decision Engine**: Churn risk classification
- **NLP Chatbot**: Natural language queries and insights
- **Sentiment Analysis**: Customer feedback analysis

---

## 🐳 Docker Deployment (Production Ready)

### Prerequisites
- Docker and Docker Compose installed
- At least 4GB RAM available
- 10GB free disk space

### Quick Start
```bash
# 1. Clone and navigate to project
git clone <your-repo-url>
cd AURA-V2

# 2. Start all services
docker-compose up -d

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f aura-app
```

### Production Configuration
```bash
# Build production image
docker build -t aura-platform:latest .

# Run with production settings
docker run -d \
  --name aura-production \
  -p 7860:7860 \
  -v $(pwd)/data:/home/aura/app/data \
  -v $(pwd)/models:/home/aura/app/models \
  -v $(pwd)/logs:/home/aura/app/logs \
  --restart unless-stopped \
  --memory 4g \
  --cpus 2 \
  aura-platform:latest
```

### Docker Services Available
- **aura-app**: Main Gradio dashboard (port 7860)
- **redis**: Caching and session management (port 6379)
- **postgres**: Database (port 5432) - optional
- **jupyter**: Data exploration (port 8888) - development only
- **prometheus**: Monitoring (port 9090) - monitoring profile
- **grafana**: Dashboards (port 3000) - monitoring profile

---

## ☁️ Cloud Deployment

### Environment Variables Required
```bash
# Core Application
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_ADDRESS=0.0.0.0

# Database (if using external DB)
DATABASE_URL=postgresql://user:password@host:port/dbname

# AI Models
PROPHET_MODEL_PATH=models/forecasting/trained_prophet_model.joblib
DECISION_RULES_PATH=models/decision_engine/rules.json
CHATBOT_KB_PATH=models/chatbot/knowledge_base.json

# Data Generation
MOCK_DATA_CUSTOMERS=500
MOCK_DATA_TRANSACTIONS_PER_CUSTOMER=10
MOCK_DATA_ENGAGEMENT_EVENTS_PER_CUSTOMER=50
```

### Cloud Provider Specific Instructions

#### AWS Deployment
```bash
# Prerequisites: AWS CLI configured
aws configure

# Run deployment script
chmod +x deploy/aws-deploy.sh
./deploy/aws-deploy.sh
```

#### Google Cloud Platform
```bash
# Prerequisites: gcloud CLI installed and authenticated
gcloud auth login

# Run deployment script
chmod +x deploy/gcp-deploy.sh
./deploy/gcp-deploy.sh
```

#### Microsoft Azure
```bash
# Prerequisites: Azure CLI installed and authenticated
az login

# Run deployment script
chmod +x deploy/azure-deploy.sh
./deploy/azure-deploy.sh
```

---

## 🔧 Configuration

### Production Environment Setup
```bash
# Create production environment file
cat > .env.production << EOF
# Database Configuration
DATABASE_URL=postgresql://aura_user:secure_password@your-db-host:5432/aura_db

# Application Settings
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_ADDRESS=0.0.0.0
DEBUG=False

# AI Model Paths
PROPHET_MODEL_PATH=models/forecasting/trained_prophet_model.joblib
DECISION_RULES_PATH=models/decision_engine/rules.json
CHATBOT_KB_PATH=models/chatbot/knowledge_base.json

# Data Settings
MOCK_DATA_CUSTOMERS=1000
MOCK_DATA_TRANSACTIONS_PER_CUSTOMER=20
MOCK_DATA_ENGAGEMENT_EVENTS_PER_CUSTOMER=100

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
EOF
```

### Monitoring and Logging
```bash
# Enable monitoring services
docker-compose --profile monitoring up -d

# Access monitoring dashboards
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/aura-admin)
```

---

## 🧪 Testing Your Deployment

### Health Checks
```bash
# Check if application is running
curl -f http://localhost:7860/ || echo "Application not responding"

# Check Docker containers
docker-compose ps

# Check logs
docker-compose logs aura-app
```

### Functional Tests
```bash
# Test data pipeline
python -c "from src.data_pipeline.orchestrator import DataPipelineOrchestrator; orchestrator = DataPipelineOrchestrator(); print('Pipeline test:', orchestrator.run_complete_pipeline())"

# Test AI models
python -c "from src.models.forecasting.prophet_model import ProphetForecastingModel; model = ProphetForecastingModel(); print('Prophet model loaded successfully')"

# Test decision engine
python -c "from src.models.decision_engine.rules_engine import RuleBasedDecisionEngine; engine = RuleBasedDecisionEngine(); print('Decision engine loaded successfully')"
```

---

## 🚨 Troubleshooting

### Common Issues

#### 1. **Port Already in Use**
```bash
# Find process using port 7860
lsof -i :7860

# Kill process
kill -9 <PID>

# Or use different port
GRADIO_SERVER_PORT=7861 python aura_gradio_app.py
```

#### 2. **Docker Build Fails**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t aura-platform .
```

#### 3. **Memory Issues**
```bash
# Increase Docker memory limit
# In Docker Desktop: Settings > Resources > Memory > 4GB

# Or run with memory limit
docker run --memory 4g aura-platform
```

#### 4. **Data Pipeline Errors**
```bash
# Check data directory permissions
ls -la data/

# Fix permissions
chmod -R 755 data/ models/ logs/
```

### Log Analysis
```bash
# View application logs
docker-compose logs -f aura-app

# View all service logs
docker-compose logs

# Check specific service
docker-compose logs redis
docker-compose logs postgres
```

---

## 📊 Performance Optimization

### Production Optimizations
```bash
# 1. Enable Redis caching
docker-compose up -d redis

# 2. Use production database
docker-compose up -d postgres

# 3. Enable monitoring
docker-compose --profile monitoring up -d

# 4. Scale application
docker-compose up -d --scale aura-app=3
```

### Resource Requirements
- **Minimum**: 2GB RAM, 2 CPU cores, 10GB storage
- **Recommended**: 4GB RAM, 4 CPU cores, 20GB storage
- **Production**: 8GB RAM, 8 CPU cores, 50GB storage

---

## 🔒 Security Considerations

### Production Security Checklist
- [ ] Change default passwords
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up SSL certificates
- [ ] Enable database encryption
- [ ] Configure backup strategies
- [ ] Set up monitoring alerts
- [ ] Implement access controls

### Environment Security
```bash
# Secure environment variables
export DATABASE_PASSWORD=$(openssl rand -base64 32)
export SECRET_KEY=$(openssl rand -base64 64)
export JWT_SECRET=$(openssl rand -base64 32)

# Use secrets management
docker secret create db_password ./secrets/db_password.txt
```

---

## 📈 Scaling Your Deployment

### Horizontal Scaling
```bash
# Scale application instances
docker-compose up -d --scale aura-app=5

# Use load balancer
docker-compose up -d nginx
```

### Vertical Scaling
```bash
# Increase container resources
docker run --memory 8g --cpus 4 aura-platform
```

### Database Scaling
```bash
# Use managed database services
# AWS RDS, GCP Cloud SQL, Azure Database
```

---

## 🆘 Support and Maintenance

### Backup Strategy
```bash
# Backup data directory
tar -czf aura-backup-$(date +%Y%m%d).tar.gz data/ models/ logs/

# Backup database
pg_dump $DATABASE_URL > aura-db-backup-$(date +%Y%m%d).sql
```

### Updates and Upgrades
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Monitoring
```bash
# Check system resources
docker stats

# Monitor logs
docker-compose logs -f

# Health checks
curl -f http://localhost:7860/health
```

---

## 🎯 Next Steps

1. **Choose your deployment method** based on your needs
2. **Set up monitoring** for production deployments
3. **Configure backups** for data protection
4. **Set up CI/CD** for automated deployments
5. **Scale as needed** based on usage

---

**🚀 Your AURA-V2 platform is ready to transform customer retention through intelligent analytics!**

*For additional support, check the troubleshooting section or create an issue in the repository.*
