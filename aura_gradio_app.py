# A.U.R.A (Adaptive User Retention Assistant) - Complete Gradio Application
# Beautiful, modern interface for customer retention analytics with all components

import gradio as gr
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import sys
import os
import logging

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import all A.U.R.A components
from src.dashboard.utils.data_loader import DashboardDataLoader
from src.dashboard.utils.plot_utils import DashboardPlotUtils
from src.data_pipeline.orchestrator import DataPipelineOrchestrator
from src.models.forecasting.prophet_model import ProphetForecastingModel
from src.models.decision_engine.rules_engine import RuleBasedDecisionEngine
from src.config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize A.U.R.A components
data_loader = DashboardDataLoader()
plot_utils = DashboardPlotUtils()
pipeline_orchestrator = DataPipelineOrchestrator()
prophet_model = ProphetForecastingModel()
decision_engine = RuleBasedDecisionEngine()

# Global variables for data storage
customer_data = pd.DataFrame()
data_loaded = False

def load_aura_data():
    """Load A.U.R.A data from pipeline or generate sample data."""
    global customer_data, data_loaded
    
    try:
        # Try to load from Gold layer first
        customer_data = data_loader.load_customer_360_data()
        if not customer_data.empty:
            data_loaded = True
            return "✅ Data loaded from A.U.R.A pipeline successfully!"
    except Exception as e:
        logger.warning(f"Pipeline data not available: {e}")
    
    # Fallback to sample data
    np.random.seed(42)
    n_customers = 500
    
    customer_data = pd.DataFrame({
        'customer_id': [f'CUST_{i:04d}' for i in range(1, n_customers + 1)],
        'name': [f'Customer {i}' for i in range(1, n_customers + 1)],
        'segment': np.random.choice(['SMB', 'Medium-Value', 'High-Value'], n_customers, p=[0.5, 0.3, 0.2]),
        'subscription_plan': np.random.choice(['Basic', 'Standard', 'Premium', 'Enterprise'], n_customers, p=[0.3, 0.4, 0.2, 0.1]),
        'current_health_score': np.clip(np.random.normal(60, 20, n_customers), 0, 100),
        'churn_risk_level': np.random.choice(['Low', 'Medium', 'High'], n_customers, p=[0.6, 0.3, 0.1]),
        'total_lifetime_revenue': np.random.lognormal(8, 1, n_customers),
        'engagement_score': np.random.uniform(0, 1, n_customers),
        'days_since_last_engagement': np.random.randint(1, 90, n_customers),
        'total_support_tickets_lifetime': np.random.poisson(3, n_customers)
    })
    
    data_loaded = True
    return "✅ Sample data generated successfully!"

def upload_and_process_csv(csv_file):
    """Upload and process CSV file through A.U.R.A pipeline."""
    global customer_data, data_loaded
    
    if csv_file is None:
        return "❌ No file uploaded. Please select a CSV file."
    
    try:
        logger.info(f"Processing uploaded CSV file: {csv_file.name}")
        
        # Read the CSV file
        uploaded_data = pd.read_csv(csv_file.name)
        
        # Validate the data
        validation_result = validate_csv_data(uploaded_data)
        if not validation_result['valid']:
            return f"❌ Data validation failed:\n{chr(10).join(validation_result['errors'])}"
        
        # Process the data through A.U.R.A pipeline
        processed_data = process_uploaded_data(uploaded_data)
        
        # Update global data
        customer_data = processed_data
        data_loaded = True
        
        return f"✅ CSV data processed successfully!\n\n**Summary:**\n- Records: {len(processed_data):,}\n- Columns: {len(processed_data.columns)}\n- Data quality: {validation_result['quality_score']:.1%}\n\n**Next steps:**\n- Explore the Dashboard tab to see your data\n- Use Customer Analysis for individual insights\n- Generate AI strategies in Retention Strategies tab"
        
    except Exception as e:
        logger.error(f"CSV processing failed: {e}")
        return f"❌ Error processing CSV file: {str(e)}"

def validate_csv_data(df):
    """Validate uploaded CSV data for A.U.R.A processing."""
    errors = []
    warnings = []
    
    # Check if DataFrame is empty
    if df.empty:
        errors.append("CSV file is empty")
        return {'valid': False, 'errors': errors, 'quality_score': 0.0}
    
    # Check for required columns (flexible requirements)
    required_columns = ['customer_id', 'name']
    missing_required = [col for col in required_columns if col not in df.columns]
    if missing_required:
        errors.append(f"Missing required columns: {missing_required}")
    
    # Check for recommended columns
    recommended_columns = ['email', 'subscription_plan', 'revenue', 'engagement_score', 'health_score']
    missing_recommended = [col for col in recommended_columns if col not in df.columns]
    if missing_recommended:
        warnings.append(f"Missing recommended columns (will use defaults): {missing_recommended}")
    
    # Check data quality
    null_percentage = df.isnull().sum().sum() / (len(df) * len(df.columns))
    quality_score = 1 - null_percentage
    
    if null_percentage > 0.5:
        errors.append(f"Too many missing values: {null_percentage:.1%}")
    elif null_percentage > 0.2:
        warnings.append(f"High missing value percentage: {null_percentage:.1%}")
    
    # Check for duplicate customer IDs
    if 'customer_id' in df.columns:
        duplicates = df['customer_id'].duplicated().sum()
        if duplicates > 0:
            warnings.append(f"Found {duplicates} duplicate customer IDs")
    
    valid = len(errors) == 0
    return {
        'valid': valid,
        'errors': errors,
        'warnings': warnings,
        'quality_score': quality_score
    }

def process_uploaded_data(df):
    """Process uploaded CSV data to match A.U.R.A format."""
    logger.info("Processing uploaded data for A.U.R.A compatibility")
    
    # Create a copy of the data
    processed_df = df.copy()
    
    # Standardize column names
    column_mapping = {
        'id': 'customer_id',
        'customer_name': 'name',
        'email_address': 'email',
        'plan': 'subscription_plan',
        'subscription': 'subscription_plan',
        'total_revenue': 'total_lifetime_revenue',
        'lifetime_revenue': 'total_lifetime_revenue',
        'revenue': 'total_lifetime_revenue',
        'health': 'current_health_score',
        'health_score': 'current_health_score',
        'engagement': 'engagement_score',
        'risk': 'churn_risk_level',
        'churn_risk': 'churn_risk_level',
        'segment': 'client_segment'
    }
    
    # Apply column mapping
    for old_name, new_name in column_mapping.items():
        if old_name in processed_df.columns and new_name not in processed_df.columns:
            processed_df[new_name] = processed_df[old_name]
    
    # Ensure required columns exist with defaults
    defaults = {
        'customer_id': lambda: [f'CUST_{i:04d}' for i in range(1, len(processed_df) + 1)],
        'name': lambda: [f'Customer {i}' for i in range(1, len(processed_df) + 1)],
        'subscription_plan': lambda: np.random.choice(['Basic', 'Standard', 'Premium', 'Enterprise'], len(processed_df)),
        'current_health_score': lambda: np.clip(np.random.normal(60, 20, len(processed_df)), 0, 100),
        'churn_risk_level': lambda: np.random.choice(['Low', 'Medium', 'High'], len(processed_df), p=[0.6, 0.3, 0.1]),
        'total_lifetime_revenue': lambda: np.random.lognormal(8, 1, len(processed_df)),
        'engagement_score': lambda: np.random.uniform(0, 1, len(processed_df)),
        'days_since_last_engagement': lambda: np.random.randint(1, 90, len(processed_df)),
        'total_support_tickets_lifetime': lambda: np.random.poisson(3, len(processed_df)),
        'segment': lambda: np.random.choice(['SMB', 'Medium-Value', 'High-Value'], len(processed_df), p=[0.5, 0.3, 0.2])
    }
    
    # Add missing columns with defaults
    for col, default_func in defaults.items():
        if col not in processed_df.columns:
            processed_df[col] = default_func()
    
    # Clean and standardize data
    processed_df['customer_id'] = processed_df['customer_id'].astype(str)
    processed_df['name'] = processed_df['name'].astype(str)
    
    # Ensure numeric columns are properly formatted
    numeric_columns = ['current_health_score', 'total_lifetime_revenue', 'engagement_score', 
                      'days_since_last_engagement', 'total_support_tickets_lifetime']
    
    for col in numeric_columns:
        if col in processed_df.columns:
            processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce').fillna(0)
    
    # Standardize categorical columns
    if 'subscription_plan' in processed_df.columns:
        processed_df['subscription_plan'] = processed_df['subscription_plan'].fillna('Basic')
    
    if 'churn_risk_level' in processed_df.columns:
        processed_df['churn_risk_level'] = processed_df['churn_risk_level'].fillna('Low')
    
    if 'segment' in processed_df.columns:
        processed_df['segment'] = processed_df['segment'].fillna('SMB')
    
    logger.info(f"Data processing completed. Final shape: {processed_df.shape}")
    return processed_df

def run_data_pipeline():
    """Run the complete A.U.R.A data pipeline."""
    try:
        logger.info("Starting A.U.R.A data pipeline execution")
        results = pipeline_orchestrator.run_complete_pipeline()
        
        if results.get('overall_success', False):
            return f"✅ Pipeline completed successfully!\n\n**Results:**\n- Bronze Records: {results['statistics']['bronze_records']:,}\n- Silver Records: {results['statistics']['silver_records']:,}\n- Gold Records: {results['statistics']['gold_records']:,}\n- Duration: {results['duration']:.2f} seconds"
        else:
            return f"⚠️ Pipeline completed with warnings.\n\n**Errors:** {len(results.get('errors', []))}\n**Warnings:** {len(results.get('warnings', []))}"
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        return f"❌ Pipeline failed: {str(e)}"

def generate_forecast(metric_type, periods):
    """Generate forecasts using Prophet model."""
    if not data_loaded or customer_data.empty:
        return None, "No data loaded. Please load data first."
    
    try:
        # Create sample time series data for demonstration
        dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
        
        if metric_type == "Revenue":
            values = np.random.lognormal(8, 1, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 1000
        elif metric_type == "Engagement":
            values = np.random.uniform(0, 1, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 30) * 0.2
        else:  # Customer Count
            values = np.random.normal(500, 50, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 100
        
        # Prepare data for Prophet
        ts_data = pd.DataFrame({
            'ds': dates,
            'y': np.clip(values, 0, None)  # Ensure positive values
        })
        
        # Train Prophet model
        prophet_model.train_model(ts_data)
        
        # Generate forecast
        forecast = prophet_model.generate_forecast(periods=int(periods))
        
        # Create visualization
        fig = prophet_model.create_forecast_visualization(forecast, ts_data)
        
        # Get insights
        insights = prophet_model.get_forecast_insights(forecast)
        
        insights_text = f"""
        **Forecast Insights for {metric_type}:**
        
        - **Forecast Periods:** {insights['forecast_summary']['total_periods']}
        - **Growth Rate:** {insights['forecast_summary']['growth_rate']:.2f}%
        - **Current Value:** {insights['forecast_summary']['current_value']:.2f}
        - **Forecasted Value:** {insights['forecast_summary']['forecasted_value']:.2f}
        
        **Recommendations:**
        {chr(10).join(f"- {rec}" for rec in insights['recommendations'])}
        """
        
        return fig, insights_text
        
    except Exception as e:
        logger.error(f"Forecast generation failed: {e}")
        return None, f"❌ Forecast generation failed: {str(e)}"

def analyze_customer_risk(customer_id):
    """Analyze customer risk using decision engine."""
    if not data_loaded or customer_data.empty:
        return "No data loaded. Please load data first."
    
    if not customer_id:
        return "Please enter a customer ID."
    
    try:
        # Find customer
        customer = customer_data[customer_data['customer_id'] == customer_id]
        if customer.empty:
            return f"Customer {customer_id} not found."
        
        customer_info = customer.iloc[0]
        
        # Analyze risk using decision engine
        risk_analysis = decision_engine.analyze_customer_risk(customer_info)
        
        # Generate recommendations
        recommendations = decision_engine.generate_recommendations(risk_analysis, customer_info)
        
        analysis_text = f"""
        ## Customer Risk Analysis: {customer_info['name']}
        
        **Customer ID:** {customer_info['customer_id']}
        **Risk Level:** {risk_analysis['risk_level']}
        **Risk Score:** {risk_analysis['composite_risk_score']:.3f}
        **Confidence:** {risk_analysis['confidence']}
        
        **Key Risk Factors:**
        {chr(10).join(f"- {factor}: {score:.3f}" for factor, score in risk_analysis['risk_factors'].items())}
        
        **Priority:** {recommendations['priority']}
        **Timeline:** {recommendations['timeline']}
        **Expected Outcome:** {recommendations['expected_outcome']}
        
        **Recommended Actions:**
        {chr(10).join(f"- {action}" for action in recommendations['recommended_actions'])}
        
        **Required Resources:**
        {chr(10).join(f"- {resource}" for resource in recommendations['resources_required'])}
        """
        
        return analysis_text
        
    except Exception as e:
        logger.error(f"Risk analysis failed: {e}")
        return f"❌ Risk analysis failed: {str(e)}"

def process_customer_batch():
    """Process all customers using decision engine."""
    if not data_loaded or customer_data.empty:
        return pd.DataFrame(), "No data loaded. Please load data first."
    
    try:
        # Process customer batch
        results = decision_engine.process_customer_batch(customer_data)
        
        # Generate summary
        summary = decision_engine.get_decision_summary(results)
        
        summary_text = f"""
        **Decision Engine Summary:**
        
        - **Total Customers:** {summary['total_customers']:,}
        - **High Risk:** {summary['high_risk_customers']:,}
        - **Critical Priority:** {summary['critical_priority_customers']:,}
        - **Average Risk Score:** {summary['average_risk_score']:.3f}
        
        **Risk Distribution:**
        {chr(10).join(f"- {level}: {count}" for level, count in summary['risk_distribution'].items())}
        
        **Priority Distribution:**
        {chr(10).join(f"- {priority}: {count}" for priority, count in summary['priority_distribution'].items())}
        
        **Key Insights:**
        {chr(10).join(f"- {insight}" for insight in summary['insights'])}
        """
        
        return results, summary_text
        
    except Exception as e:
        logger.error(f"Batch processing failed: {e}")
        return pd.DataFrame(), f"❌ Batch processing failed: {str(e)}"

def get_metrics():
    """Get key metrics for the dashboard."""
    if not data_loaded or customer_data.empty:
        return "No data loaded", "No data loaded", "No data loaded", "No data loaded"
    
    total_customers = len(customer_data)
    high_risk = len(customer_data[customer_data.get('churn_risk_level', '') == 'High'])
    avg_health = customer_data.get('current_health_score', pd.Series([0])).mean()
    total_revenue = customer_data.get('total_lifetime_revenue', pd.Series([0])).sum()
    
    return (
        f"{total_customers:,}",
        f"{high_risk:,}",
        f"{avg_health:.1f}",
        f"${total_revenue:,.0f}"
    )

def create_risk_distribution_chart():
    """Create risk distribution pie chart."""
    if not data_loaded or customer_data.empty:
        return None
    
    risk_data = customer_data.get('churn_risk_level', customer_data.get('churn_risk', ''))
    if risk_data.empty:
        return None
    
    risk_counts = risk_data.value_counts()
    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title="Customer Risk Distribution",
        color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
    )
    fig.update_layout(
        title_font_size=16,
        font=dict(size=12)
    )
    return fig

def create_health_score_chart():
    """Create health score distribution histogram."""
    if not data_loaded or customer_data.empty:
        return None
    
    health_data = customer_data.get('current_health_score', customer_data.get('health_score', pd.Series([0])))
    if health_data.empty:
        return None
    
    fig = px.histogram(
        customer_data,
        x=health_data.name,
        nbins=20,
        title="Health Score Distribution",
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(
        title_font_size=16,
        font=dict(size=12)
    )
    return fig

def create_segment_chart():
    """Create customer segment bar chart."""
    if not data_loaded or customer_data.empty:
        return None
    
    segment_data = customer_data.get('segment', '')
    if segment_data.empty:
        return None
    
    segment_counts = segment_data.value_counts()
    fig = px.bar(
        x=segment_counts.index,
        y=segment_counts.values,
        title="Customer Segments",
        color_discrete_sequence=['#764ba2']
    )
    fig.update_layout(
        title_font_size=16,
        font=dict(size=12)
    )
    return fig

def get_customer_table():
    """Get customer data table."""
    if not data_loaded or customer_data.empty:
        return pd.DataFrame()
    
    display_cols = ['customer_id', 'name', 'segment', 'subscription_plan', 'current_health_score', 'churn_risk_level']
    available_cols = [col for col in display_cols if col in customer_data.columns]
    return customer_data[available_cols].head(20)

def analyze_customer(customer_id):
    """Analyze a specific customer."""
    if not data_loaded or customer_data.empty:
        return "No data loaded. Please load data first."
    
    if not customer_id:
        return "Please enter a customer ID."
    
    # Find customer
    customer = customer_data[customer_data['customer_id'] == customer_id]
    if customer.empty:
        return f"Customer {customer_id} not found."
    
    customer_info = customer.iloc[0]
    
    # Create analysis
    analysis = f"""
    ## Customer Analysis: {customer_info['name']}
    
    **Customer ID:** {customer_info['customer_id']}
    **Segment:** {customer_info.get('segment', 'N/A')}
    **Subscription Plan:** {customer_info.get('subscription_plan', 'N/A')}
    **Health Score:** {customer_info.get('current_health_score', 'N/A')}
    **Churn Risk:** {customer_info.get('churn_risk_level', 'N/A')}
    **Lifetime Revenue:** ${customer_info.get('total_lifetime_revenue', 0):,.2f}
    **Engagement Score:** {customer_info.get('engagement_score', 0):.2f}
    **Days Since Last Engagement:** {customer_info.get('days_since_last_engagement', 'N/A')}
    **Support Tickets:** {customer_info.get('total_support_tickets_lifetime', 'N/A')}
    
    ### Recommendations:
    """
    
    # Add recommendations based on data
    if customer_info.get('churn_risk_level') == 'High':
        analysis += "\n- ⚠️ **High churn risk detected** - Immediate intervention needed"
        analysis += "\n- 📞 Schedule retention call with customer success team"
        analysis += "\n- 🎯 Offer personalized incentives or discounts"
    
    if customer_info.get('current_health_score', 0) < 50:
        analysis += "\n- 📈 **Low health score** - Focus on engagement improvement"
        analysis += "\n- 📚 Provide additional training and resources"
        analysis += "\n- 🤝 Assign dedicated customer success manager"
    
    if customer_info.get('days_since_last_engagement', 0) > 30:
        analysis += "\n- ⏰ **Low recent engagement** - Re-engagement campaign needed"
        analysis += "\n- 📧 Send personalized re-engagement emails"
        analysis += "\n- 🎪 Invite to upcoming webinars or events"
    
    return analysis

def get_retention_strategies():
    """Get retention strategies based on current data."""
    if not data_loaded or customer_data.empty:
        return "No data loaded. Please load data first."
    
    strategies = """
    ## 🎯 A.U.R.A Retention Strategies
    
    ### High-Risk Customer Intervention
    - **Immediate Action Required:** {high_risk_count} customers at high churn risk
    - **Strategy:** Proactive outreach with personalized retention offers
    - **Timeline:** Within 48 hours
    
    ### Health Score Improvement
    - **Focus Area:** {low_health_count} customers with health scores below 50
    - **Strategy:** Enhanced onboarding and success management
    - **Timeline:** 2-4 weeks improvement cycle
    
    ### Engagement Recovery
    - **Target:** {low_engagement_count} customers with low recent engagement
    - **Strategy:** Multi-channel re-engagement campaigns
    - **Timeline:** 1-2 weeks campaign duration
    
    ### Revenue Optimization
    - **Opportunity:** {upsell_candidates} customers ready for plan upgrades
    - **Strategy:** Value-based upselling with ROI demonstrations
    - **Timeline:** Next billing cycle
    """.format(
        high_risk_count=len(customer_data[customer_data.get('churn_risk_level', '') == 'High']),
        low_health_count=len(customer_data[customer_data.get('current_health_score', 100) < 50]),
        low_engagement_count=len(customer_data[customer_data.get('days_since_last_engagement', 0) > 30]),
        upsell_candidates=len(customer_data[customer_data.get('current_health_score', 0) > 80])
    )
    
    return strategies

def chat_with_aura(message, history):
    """Chat with A.U.R.A AI assistant."""
    if not message:
        return history, ""
    
    # Simple AI responses based on keywords
    message_lower = message.lower()
    
    if "churn" in message_lower or "retention" in message_lower:
        response = "I can help you analyze churn risk and retention strategies. Based on your current data, I recommend focusing on high-risk customers first."
    elif "health" in message_lower or "score" in message_lower:
        response = "Health scores indicate customer satisfaction and engagement levels. Customers with scores below 50 need immediate attention."
    elif "revenue" in message_lower or "upsell" in message_lower:
        response = "Revenue optimization opportunities exist among high-health-score customers. Consider targeted upselling campaigns."
    elif "engagement" in message_lower:
        response = "Engagement metrics show customer activity levels. Low engagement often precedes churn - implement re-engagement campaigns."
    elif "help" in message_lower or "what" in message_lower:
        response = "I'm A.U.R.A, your Adaptive User Retention Assistant. I can help with churn analysis, retention strategies, customer health monitoring, and revenue optimization. What would you like to know?"
    else:
        response = "I understand you're asking about customer retention. Could you be more specific about what aspect you'd like help with?"
    
    history.append([message, response])
    return history, ""

# Create the Gradio interface
with gr.Blocks(
    title="A.U.R.A - Adaptive User Retention Assistant",
    theme=gr.themes.Soft(
        primary_hue=gr.themes.Color(c50="#F8C662", c100="#F8C662", c200="#F8C662", c300="#F8C662", c400="#F8C662", c500="#595082", c600="#595082", c700="#2C263F", c800="#2C263F", c900="#2C263F", c950="#2C263F"),
        secondary_hue=gr.themes.Color(c50="#41644A", c100="#41644A", c200="#41644A", c300="#41644A", c400="#41644A", c500="#213722", c600="#213722", c700="#213722", c800="#213722", c900="#213722", c950="#213722"),
        neutral_hue=gr.themes.Color(c50="#F8C662", c100="#F8C662", c200="#595082", c300="#595082", c400="#41644A", c500="#2C263F", c600="#2C263F", c700="#213722", c800="#213722", c900="#213722", c950="#213722"),
    ),
    css="""
    .gradio-container {
        background: linear-gradient(135deg, #2C263F 0%, #595082 30%, #41644A 70%, #213722 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    .gr-panel {
        background: rgba(248, 198, 98, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(44, 38, 63, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(89, 80, 130, 0.4);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2C263F;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(44, 38, 63, 0.2);
    }
    .gr-button {
        background: linear-gradient(135deg, #2C263F 0%, #595082 100%);
        color: #F8C662;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(44, 38, 63, 0.4);
        border: none;
    }
    .gr-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(44, 38, 63, 0.5);
        background: linear-gradient(135deg, #595082 0%, #41644A 100%);
    }
    .gr-tab-button.selected {
        background: linear-gradient(135deg, #2C263F 0%, #595082 100%);
        color: #F8C662;
        border-radius: 8px;
    }
    .gr-tab-button {
        color: #2C263F;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .gr-tab-button:hover {
        background: rgba(65, 100, 74, 0.15);
        color: #41644A;
    }
    .gr-textbox, .gr-dropdown, .gr-slider {
        border: 2px solid rgba(89, 80, 130, 0.4);
        border-radius: 8px;
        background: rgba(248, 198, 98, 0.9);
    }
    .gr-textbox:focus, .gr-dropdown:focus {
        border-color: #41644A;
        box-shadow: 0 0 0 3px rgba(65, 100, 74, 0.2);
    }
    .gr-plot {
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(44, 38, 63, 0.2);
    }
    .gr-dataframe {
        border-radius: 12px;
        border: 1px solid rgba(89, 80, 130, 0.4);
    }
    .gr-chatbot {
        border-radius: 12px;
        border: 1px solid rgba(89, 80, 130, 0.4);
        background: rgba(248, 198, 98, 0.9);
    }
    """
) as app:
    
    # Header
    gr.Markdown(
        """
        # 🤖 A.U.R.A - Adaptive User Retention Assistant
        
        **Adaptive User Retention Assistant Platform** - Advanced customer analytics and retention strategies powered by AI.
        """,
        elem_classes=["header"]
    )
    
    # Main tabs
    with gr.Tabs():
        
        # Dashboard Tab
        with gr.Tab("📊 Dashboard"):
            gr.Markdown("## Executive Dashboard")
            
            # Data loading section
            with gr.Row():
                load_btn = gr.Button("🔄 Load A.U.R.A Data", variant="primary")
                pipeline_btn = gr.Button("⚙️ Run Data Pipeline", variant="secondary")
                status_text = gr.Textbox(label="Status", interactive=False)
            
            # CSV Upload section
            gr.Markdown("### 📁 Upload Your Own Data")
            with gr.Row():
                csv_upload = gr.File(
                    label="Upload CSV File",
                    file_types=[".csv"],
                    file_count="single"
                )
                upload_btn = gr.Button("📤 Process CSV Data", variant="primary")
            
            # CSV format guidance
            gr.Markdown("""
            **📋 CSV Format Requirements:**
            
            **Required Columns:**
            - `customer_id` (or `id`) - Unique customer identifier
            - `name` (or `customer_name`) - Customer name
            
            **Recommended Columns:**
            - `email` - Customer email address
            - `subscription_plan` (or `plan`) - Subscription tier
            - `revenue` (or `total_revenue`) - Customer revenue
            - `engagement_score` - Customer engagement level (0-1)
            - `health_score` - Customer health score (0-100)
            - `churn_risk_level` - Risk level (Low/Medium/High)
            - `segment` - Customer segment
            
            **💡 Tips:**
            - Missing recommended columns will be filled with realistic defaults
            - Data will be automatically cleaned and standardized
            - Supports various column name formats (e.g., 'id' → 'customer_id')
            """)
            
            # Sample CSV download
            with gr.Row():
                gr.Markdown("**📥 Need a template?** Download our sample CSV file:")
                sample_csv = gr.File(
                    label="Download Sample CSV",
                    value="sample_customer_data.csv",
                    visible=True,
                    interactive=False
                )
            
            load_btn.click(
                load_aura_data,
                outputs=[status_text]
            )
            
            pipeline_btn.click(
                run_data_pipeline,
                outputs=[status_text]
            )
            
            upload_btn.click(
                upload_and_process_csv,
                inputs=[csv_upload],
                outputs=[status_text]
            )
            
            # Metrics row
            with gr.Row():
                total_customers = gr.Textbox(label="Total Customers", interactive=False)
                high_risk = gr.Textbox(label="High Risk Customers", interactive=False)
                avg_health = gr.Textbox(label="Average Health Score", interactive=False)
                total_revenue = gr.Textbox(label="Total Revenue", interactive=False)
            
            # Charts row
            with gr.Row():
                with gr.Column():
                    risk_chart = gr.Plot(label="Risk Distribution")
                with gr.Column():
                    health_chart = gr.Plot(label="Health Score Distribution")
            
            # Segment chart
            segment_chart = gr.Plot(label="Customer Segments")
            
            # Customer table
            customer_table = gr.Dataframe(
                label="Customer Overview",
                interactive=False,
                wrap=True
            )
            
            # Update dashboard when data is loaded
            load_btn.click(
                get_metrics,
                outputs=[total_customers, high_risk, avg_health, total_revenue]
            )
            
            load_btn.click(
                create_risk_distribution_chart,
                outputs=[risk_chart]
            )
            
            load_btn.click(
                create_health_score_chart,
                outputs=[health_chart]
            )
            
            load_btn.click(
                create_segment_chart,
                outputs=[segment_chart]
            )
            
            load_btn.click(
                get_customer_table,
                outputs=[customer_table]
            )
        
        # Customer Analysis Tab
        with gr.Tab("👥 Customer Analysis"):
            gr.Markdown("## Individual Customer Analysis")
            
            customer_id_input = gr.Textbox(
                label="Customer ID",
                placeholder="Enter customer ID (e.g., CUST_0001)",
                info="Enter a customer ID to analyze their profile and get recommendations"
            )
            
            analyze_btn = gr.Button("🔍 Analyze Customer", variant="primary")
            
            customer_analysis = gr.Markdown(label="Customer Analysis")
            
            analyze_btn.click(
                analyze_customer,
                inputs=[customer_id_input],
                outputs=[customer_analysis]
            )
        
        # Retention Strategies Tab
        with gr.Tab("💡 Retention Strategies"):
            gr.Markdown("## AI-Powered Retention Strategies")
            
            strategies_btn = gr.Button("🎯 Generate Strategies", variant="primary")
            
            retention_strategies = gr.Markdown(label="Retention Strategies")
            
            strategies_btn.click(
                get_retention_strategies,
                outputs=[retention_strategies]
            )
        
        # Forecasting Tab
        with gr.Tab("📈 Forecasting"):
            gr.Markdown("## AI-Powered Forecasting with Prophet")
            
            with gr.Row():
                metric_type = gr.Dropdown(
                    choices=["Revenue", "Engagement", "Customer Count"],
                    label="Metric to Forecast",
                    value="Revenue"
                )
                periods = gr.Slider(
                    minimum=7,
                    maximum=365,
                    value=30,
                    step=1,
                    label="Forecast Periods (Days)"
                )
                forecast_btn = gr.Button("🔮 Generate Forecast", variant="primary")
            
            forecast_plot = gr.Plot(label="Forecast Visualization")
            forecast_insights = gr.Markdown(label="Forecast Insights")
            
            forecast_btn.click(
                generate_forecast,
                inputs=[metric_type, periods],
                outputs=[forecast_plot, forecast_insights]
            )
        
        # Risk Analysis Tab
        with gr.Tab("⚠️ Risk Analysis"):
            gr.Markdown("## AI-Powered Risk Analysis")
            
            with gr.Row():
                risk_customer_id = gr.Textbox(
                    label="Customer ID",
                    placeholder="Enter customer ID (e.g., CUST_0001)",
                    scale=2
                )
                analyze_risk_btn = gr.Button("🔍 Analyze Risk", variant="primary", scale=1)
            
            risk_analysis = gr.Markdown(label="Risk Analysis Results")
            
            analyze_risk_btn.click(
                analyze_customer_risk,
                inputs=[risk_customer_id],
                outputs=[risk_analysis]
            )
            
            # Batch processing section
            gr.Markdown("### Batch Risk Analysis")
            batch_btn = gr.Button("📊 Process All Customers", variant="secondary")
            
            batch_results = gr.Dataframe(
                label="Batch Analysis Results",
                interactive=False,
                wrap=True
            )
            batch_summary = gr.Markdown(label="Batch Analysis Summary")
            
            batch_btn.click(
                process_customer_batch,
                outputs=[batch_results, batch_summary]
            )
        
        # AI Assistant Tab
        with gr.Tab("🤖 AI Assistant"):
            gr.Markdown("## Chat with A.U.R.A AI Assistant")
            
            chatbot = gr.Chatbot(
                label="A.U.R.A Assistant",
                type="messages",
                height=400
            )
            
            with gr.Row():
                msg_input = gr.Textbox(
                    label="Ask A.U.R.A anything about customer retention",
                    placeholder="Ask about churn analysis, retention strategies, or customer health...",
                    scale=4
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)
            
            # Chat functionality
            msg_input.submit(
                chat_with_aura,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, msg_input]
            )
            
            send_btn.click(
                chat_with_aura,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, msg_input]
            )
    
    # Footer
    gr.Markdown(
        f"""
        ---
        <div style="text-align: center; color: #666; font-size: 0.9em;">
        🤖 A.U.R.A - Adaptive User Retention Assistant | Built with Gradio | Version {settings.PROJECT_VERSION}
        </div>
        """,
        elem_classes=["footer"]
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )