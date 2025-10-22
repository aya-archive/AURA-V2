# 🤖 A.U.R.A - Adaptive User Retention Assistant

**Intelligent Customer Retention Analytics Platform**

A.U.R.A is a comprehensive AI-powered platform that empowers businesses to predict, prevent, and optimize customer retention through intelligent analytics, automated insights, and actionable recommendations.

## 🎯 Mission

Transform customer retention from reactive to proactive by leveraging AI and machine learning to identify at-risk customers, predict churn patterns, and recommend personalized retention strategies.

## 🚀 Key Features

### 📊 Intelligent Dashboard
- **Real-time Customer Health Monitoring**: Live dashboards with health scores and risk indicators
- **Predictive Analytics**: AI-powered churn prediction and trend forecasting
- **Interactive Visualizations**: Dynamic charts, graphs, and data exploration tools
- **KPI Tracking**: Comprehensive metrics for retention, engagement, and revenue

### 💡 Strategy Playbook
- **Comprehensive Retention Strategies**: 10+ proven strategies with implementation guidance
- **Personalized Recommendations**: AI-driven strategy suggestions based on customer profiles
- **Success Metrics**: ROI analysis and performance tracking for each strategy
- **Implementation Guidance**: Step-by-step instructions and resource requirements

### 🤖 AI Chatbot
- **Natural Language Queries**: Ask questions about your data in plain English
- **Intelligent Insights**: AI-powered analysis and recommendations
- **Strategy Simulation**: Test different approaches and predict outcomes
- **Data Exploration**: Interactive data analysis and visualization

### 🔄 Data Pipeline
- **Bronze Layer**: Raw data ingestion from multiple sources
- **Silver Layer**: Data cleaning, transformation, and enrichment
- **Gold Layer**: Business-ready analytics and insights
- **Automated Processing**: End-to-end data pipeline with monitoring and alerts

## 🏗️ Architecture

### Data Architecture (Medallion Pattern)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Bronze Layer  │───▶│   Silver Layer  │───▶│    Gold Layer   │
│                 │    │                 │    │                 │
│ • Raw Data      │    │ • Cleaned Data  │    │ • Analytics     │
│ • CSV Files     │    │ • Enriched Data │    │ • KPIs          │
│ • Logs          │    │ • Derived Metrics│   │ • Insights      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### AI Models
- **Prophet Forecasting**: Time series prediction for revenue and engagement trends
- **Rule-based Decision Engine**: Churn risk classification and recommendation generation
- **NLP Chatbot**: Intent recognition and natural language processing
- **Sentiment Analysis**: Customer feedback and support ticket analysis

### Technology Stack
- **Backend**: Python 3.8+, Pandas, NumPy, Scikit-learn
- **Frontend**: Gradio, Streamlit, Plotly, Matplotlib
- **AI/ML**: Prophet, Transformers, Sentence-Transformers
- **Data**: Parquet, CSV, JSON
- **Deployment**: Gradio Spaces, Streamlit Cloud, Docker

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/aura-v2.git
   cd aura-v2
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample data**
   ```bash
   python generate_mock_data.py
   ```

4. **Run the data pipeline**
   ```bash
   python -c "from src.data_pipeline.orchestrator import DataPipelineOrchestrator; orchestrator = DataPipelineOrchestrator(); orchestrator.run_complete_pipeline()"
   ```

5. **Launch the application**
   
   **Gradio Interface (Recommended):**
   ```bash
   python3 aura_gradio_app.py
   ```
   
   **Streamlit Interface:**
   ```bash
   streamlit run src/dashboard/app.py
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t aura-platform .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 aura-platform
   ```

## 📊 Data Sources

The platform processes data from multiple sources:

- **Customer Demographics**: Basic customer information and subscription details
- **Transaction History**: Payment records, revenue data, and billing information
- **Engagement Logs**: User interactions, feature usage, and activity tracking
- **Support Interactions**: Support tickets, chat logs, and customer service data
- **Feedback Surveys**: NPS scores, satisfaction ratings, and customer feedback

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/dbname

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# AI Model Configuration
PROPHET_MODEL_PATH=models/forecasting/trained_prophet_model.joblib
DECISION_RULES_PATH=models/decision_engine/rules.json
CHATBOT_KB_PATH=models/chatbot/knowledge_base.json

# Data Generation
MOCK_DATA_CUSTOMERS=500
MOCK_DATA_TRANSACTIONS_PER_CUSTOMER=10
MOCK_DATA_ENGAGEMENT_EVENTS_PER_CUSTOMER=50
```

### Streamlit Configuration
The platform includes custom Streamlit theming in `.streamlit/config.toml`:

- **A.U.R.A Brand Colors**: Deep blue (#004D7A) and teal (#00B3B3) color scheme
- **Custom Typography**: Lato font family for modern, clean appearance
- **Responsive Design**: Mobile-friendly layout and components
- **Accessibility**: WCAG AA compliance and keyboard navigation

## 🧪 Testing

### Run Unit Tests
```bash
# Data Pipeline Tests
python -m pytest src/tests/unit/test_data_pipeline.py -v

# Model Tests
python -m pytest src/tests/unit/test_models.py -v

# All Tests
python -m pytest src/tests/ -v
```

### Run Integration Tests
```bash
python -m pytest src/tests/integration/ -v
```

### Test Coverage
```bash
python -m pytest --cov=src --cov-report=html
```

## 📈 Usage Examples

### Gradio Interface (Recommended)
The modern Gradio interface provides 6 main tabs:

#### 📊 Dashboard Tab
- **Load Data**: Click "Load A.U.R.A Data" to load customer data or generate sample data
- **Run Pipeline**: Click "Run Data Pipeline" to execute the complete Bronze/Silver/Gold pipeline
- **View Metrics**: Real-time KPIs including total customers, high-risk count, average health score
- **Interactive Charts**: Risk distribution, health score distribution, and customer segments

#### 👥 Customer Analysis Tab
- **Individual Analysis**: Enter a customer ID to get detailed analysis and recommendations
- **Customer Overview**: View comprehensive customer profiles with health scores and risk levels

#### 💡 Retention Strategies Tab
- **AI Recommendations**: Get personalized retention strategies based on customer data
- **Strategy Implementation**: Step-by-step guidance for implementing retention programs

#### 📈 Forecasting Tab
- **Time Series Prediction**: Use Prophet model to forecast revenue, engagement, or customer count
- **Interactive Controls**: Select metric type and forecast periods (7-365 days)
- **Visual Insights**: Interactive charts with confidence intervals and trend analysis

#### ⚠️ Risk Analysis Tab
- **Individual Risk Assessment**: Analyze specific customers using the decision engine
- **Batch Processing**: Process all customers for comprehensive risk analysis
- **Priority Classification**: Get priority levels and recommended actions for each customer

#### 🤖 AI Assistant Tab
- **Natural Language Queries**: Ask questions like "Show me high-risk customers"
- **Data Insights**: Request analysis like "What's our churn risk distribution?"
- **Strategy Advice**: Get recommendations like "What strategies should I use?"
- **Interactive Chat**: Conversational AI for data exploration and insights

### Streamlit Interface (Legacy)
1. **Load Data**: Use the sidebar to load customer data or generate sample data
2. **Apply Filters**: Filter by risk level, customer segment, or date range
3. **Explore Insights**: View executive summary, risk analysis, and customer details
4. **Monitor KPIs**: Track key metrics and trends in real-time

## 🔒 Security & Privacy

- **Local Processing**: All data processing happens locally on your infrastructure
- **No External APIs**: No data is sent to external services or third parties
- **Secure Storage**: Data is stored securely with access controls
- **Privacy Compliance**: GDPR and privacy regulation compliant
- **Audit Logging**: Comprehensive logging for security and compliance

## 🚀 Deployment

### Streamlit Cloud
1. **Connect Repository**: Link your GitHub repository to Streamlit Cloud
2. **Configure Secrets**: Set up environment variables in Streamlit Cloud
3. **Deploy**: Automatic deployment with custom domain support

### Docker Deployment
1. **Build Image**: Use the provided Dockerfile for containerized deployment
2. **Environment Variables**: Configure through Docker environment or secrets
3. **Scale**: Deploy multiple instances with load balancing

### Local Development
1. **Development Mode**: Run with `streamlit run src/dashboard/app.py --server.runOnSave true`
2. **Hot Reload**: Automatic reloading on code changes
3. **Debug Mode**: Enable detailed logging and error reporting

## 📚 API Documentation

### Data Pipeline API
```python
from src.data_pipeline.orchestrator import DataPipelineOrchestrator

# Run complete pipeline
orchestrator = DataPipelineOrchestrator()
results = orchestrator.run_complete_pipeline()
```

### Forecasting API
```python
from src.models.forecasting.prophet_model import ProphetForecasting

# Train and predict
forecasting = ProphetForecasting()
model = forecasting.train_model(data)
predictions = forecasting.make_predictions(model, periods=30)
```

### Rules Engine API
```python
from src.models.decision_engine.rules_engine import RulesEngine

# Classify and recommend
rules_engine = RulesEngine()
risk_level = rules_engine.classify_churn_risk(customer_data)
recommendations = rules_engine.generate_recommendations(customer_data)
```

## 🤝 Contributing

1. **Fork the Repository**: Create your own fork of the project
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**: Submit a pull request for review

### Development Guidelines
- **Code Style**: Follow PEP 8 and use Black for formatting
- **Testing**: Write tests for all new features and bug fixes
- **Documentation**: Update documentation for any changes
- **Type Hints**: Use type hints for better code clarity

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- **User Guide**: Comprehensive user documentation and tutorials
- **API Reference**: Detailed API documentation and examples
- **Troubleshooting**: Common issues and solutions

### Community
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Community discussions and Q&A
- **Contributing**: Guidelines for contributing to the project

### Professional Support
- **Enterprise Support**: Dedicated support for enterprise deployments
- **Custom Development**: Tailored solutions for specific business needs
- **Training**: Comprehensive training programs for teams

## 🎯 Roadmap

### Version 1.1 (Q2 2024)
- [ ] Advanced ML models (XGBoost, Neural Networks)
- [ ] Real-time data streaming
- [ ] Advanced analytics and reporting
- [ ] Mobile application

### Version 1.2 (Q3 2024)
- [ ] Multi-tenant support
- [ ] Advanced security features
- [ ] API integrations
- [ ] Custom model training

### Version 2.0 (Q4 2024)
- [ ] Advanced AI capabilities
- [ ] Predictive maintenance
- [ ] Automated strategy execution
- [ ] Enterprise features

## 🙏 Acknowledgments

- **Streamlit Team**: For the amazing web framework
- **Prophet Team**: For the powerful forecasting library
- **Open Source Community**: For the incredible tools and libraries
- **Contributors**: For their valuable contributions and feedback

---

**Built with ❤️ by the A.U.R.A Team**

*Transforming customer retention through intelligent analytics*