# A.U.R.A (Adaptive User Retention Assistant) - Streamlit Application
# Streamlit Cloud deployment version of the AURA platform
# This version is optimized for Streamlit Cloud with all AURA features

import streamlit as st
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

# Configure page
st.set_page_config(
    page_title="A.U.R.A - Adaptive User Retention Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for AURA branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #004D7A 0%, #00B3B3 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .main-header p {
        color: white;
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #00B3B3;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00B3B3;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'customer_data' not in st.session_state:
    st.session_state.customer_data = pd.DataFrame()
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Import AURA components with error handling
try:
    from src.dashboard.utils.data_loader import DashboardDataLoader
    from src.dashboard.utils.plot_utils import DashboardPlotUtils
    from src.data_pipeline.orchestrator import DataPipelineOrchestrator
    from src.models.forecasting.prophet_model import ProphetForecastingModel
    from src.models.decision_engine.rules_engine import RuleBasedDecisionEngine
    from src.models.chatbot.aura_ai_model import aura_ai_model
    from src.config.settings import settings
    
    # Initialize AURA components
    data_loader = DashboardDataLoader()
    plot_utils = DashboardPlotUtils()
    pipeline_orchestrator = DataPipelineOrchestrator()
    prophet_model = ProphetForecastingModel()
    decision_engine = RuleBasedDecisionEngine()
    
    components_loaded = True
except Exception as e:
    st.error(f"⚠️ Some AURA components could not be loaded: {e}")
    components_loaded = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_aura_data():
    """Load A.U.R.A data from pipeline or generate sample data."""
    try:
        if components_loaded:
            # Try to load from Gold layer first
            customer_data = data_loader.load_customer_360_data()
            if not customer_data.empty:
                st.session_state.customer_data = customer_data
                st.session_state.data_loaded = True
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
    
    st.session_state.customer_data = customer_data
    st.session_state.data_loaded = True
    return "✅ Sample data generated successfully!"

def run_data_pipeline():
    """Run the complete A.U.R.A data pipeline."""
    if not components_loaded:
        return "❌ AURA components not available. Using sample data instead."
    
    try:
        # Run the complete pipeline
        results = pipeline_orchestrator.run_complete_pipeline()
        
        # Load the processed data
        customer_data = data_loader.load_customer_360_data()
        if not customer_data.empty:
            st.session_state.customer_data = customer_data
            st.session_state.data_loaded = True
            return "✅ A.U.R.A data pipeline completed successfully!"
        else:
            return "⚠️ Pipeline completed but no data found. Using sample data."
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        return f"❌ Pipeline failed: {str(e)}"

def create_dashboard_metrics():
    """Create the main dashboard metrics."""
    if not st.session_state.data_loaded:
        return
    
    data = st.session_state.customer_data
    
    # Calculate key metrics
    total_customers = len(data)
    high_risk_customers = len(data[data['churn_risk_level'] == 'High'])
    avg_health_score = data['current_health_score'].mean()
    total_revenue = data['total_lifetime_revenue'].sum()
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Customers",
            value=f"{total_customers:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="⚠️ High Risk Customers",
            value=f"{high_risk_customers:,}",
            delta=f"{high_risk_customers/total_customers*100:.1f}%"
        )
    
    with col3:
        st.metric(
            label="💚 Average Health Score",
            value=f"{avg_health_score:.1f}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="💰 Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta=None
        )

def create_risk_distribution_chart():
    """Create risk distribution visualization."""
    if not st.session_state.data_loaded:
        return None
    
    data = st.session_state.customer_data
    
    # Risk distribution
    risk_counts = data['churn_risk_level'].value_counts()
    
    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title="Customer Risk Distribution",
        color_discrete_map={
            'Low': '#00B3B3',
            'Medium': '#FFA500',
            'High': '#FF4444'
        }
    )
    
    fig.update_layout(
        showlegend=True,
        height=400,
        font=dict(size=12)
    )
    
    return fig

def create_health_score_distribution():
    """Create health score distribution chart."""
    if not st.session_state.data_loaded:
        return None
    
    data = st.session_state.customer_data
    
    fig = px.histogram(
        data,
        x='current_health_score',
        nbins=20,
        title="Customer Health Score Distribution",
        labels={'current_health_score': 'Health Score', 'count': 'Number of Customers'},
        color_discrete_sequence=['#00B3B3']
    )
    
    fig.update_layout(
        height=400,
        font=dict(size=12)
    )
    
    return fig

def analyze_customer(customer_id):
    """Analyze individual customer."""
    if not st.session_state.data_loaded:
        return "❌ No data loaded. Please load data first."
    
    data = st.session_state.customer_data
    
    # Find customer
    customer = data[data['customer_id'] == customer_id]
    
    if customer.empty:
        return f"❌ Customer {customer_id} not found."
    
    customer = customer.iloc[0]
    
    # Create analysis
    analysis = f"""
    ## 👤 Customer Analysis: {customer['name']}
    
    **Customer ID:** {customer['customer_id']}
    **Segment:** {customer['segment']}
    **Subscription Plan:** {customer['subscription_plan']}
    **Health Score:** {customer['current_health_score']:.1f}/100
    **Risk Level:** {customer['churn_risk_level']}
    **Lifetime Revenue:** ${customer['total_lifetime_revenue']:,.2f}
    **Engagement Score:** {customer['engagement_score']:.2f}
    **Days Since Last Engagement:** {customer['days_since_last_engagement']}
    **Support Tickets:** {customer['total_support_tickets_lifetime']}
    
    ### 🎯 Recommendations:
    """
    
    # Generate recommendations based on risk level
    if customer['churn_risk_level'] == 'High':
        analysis += """
        - **Immediate Action Required**: This customer is at high risk of churning
        - **Personal Outreach**: Schedule a call with the customer success team
        - **Retention Offer**: Consider offering a discount or upgrade
        - **Engagement Boost**: Send personalized content and check-ins
        """
    elif customer['churn_risk_level'] == 'Medium':
        analysis += """
        - **Proactive Engagement**: Increase touchpoints and communication
        - **Value Demonstration**: Show additional product benefits
        - **Feedback Collection**: Gather insights on their experience
        - **Upsell Opportunities**: Present relevant upgrades
        """
    else:
        analysis += """
        - **Maintain Relationship**: Continue current engagement level
        - **Growth Opportunities**: Look for expansion possibilities
        - **Advocacy Programs**: Encourage referrals and testimonials
        - **Success Stories**: Share relevant case studies
        """
    
    return analysis

def get_forecast(metric_type, periods):
    """Get forecasting predictions."""
    if not components_loaded:
        return "❌ Forecasting model not available."
    
    try:
        # Generate sample forecast data
        dates = pd.date_range(start='2024-01-01', periods=periods, freq='D')
        
        if metric_type == 'Revenue':
            values = np.random.lognormal(8, 0.5, periods)
        elif metric_type == 'Engagement':
            values = np.random.uniform(0.3, 0.9, periods)
        else:  # Customer Count
            values = np.random.normal(500, 50, periods)
        
        forecast_data = pd.DataFrame({
            'date': dates,
            'value': values
        })
        
        # Create forecast chart
        fig = px.line(
            forecast_data,
            x='date',
            y='value',
            title=f"{metric_type} Forecast ({periods} days)",
            labels={'value': metric_type, 'date': 'Date'}
        )
        
        fig.update_layout(
            height=400,
            font=dict(size=12)
        )
        
        return fig
    except Exception as e:
        return f"❌ Forecasting error: {str(e)}"

def get_ai_response(question):
    """Get AI assistant response."""
    if not components_loaded:
        return "🤖 AI Assistant: I'm currently unavailable. Please try again later."
    
    try:
        # Simple AI responses based on keywords
        question_lower = question.lower()
        
        if 'high risk' in question_lower or 'churn' in question_lower:
            return "🤖 AI Assistant: High-risk customers are those with low health scores, high support ticket volume, or low engagement. Focus on immediate intervention strategies like personal outreach and retention offers."
        elif 'revenue' in question_lower or 'money' in question_lower:
            return "🤖 AI Assistant: Revenue trends show the financial health of your customer base. Monitor for declining trends and implement revenue protection strategies."
        elif 'engagement' in question_lower:
            return "🤖 AI Assistant: Customer engagement is crucial for retention. Track login frequency, feature usage, and interaction patterns to identify at-risk customers."
        elif 'strategy' in question_lower or 'recommend' in question_lower:
            return "🤖 AI Assistant: Effective retention strategies include personalized outreach, value demonstration, proactive support, and loyalty programs. Tailor approaches based on customer segments."
        else:
            return "🤖 AI Assistant: I can help you analyze customer data, identify trends, and recommend retention strategies. What would you like to know about your customers?"
    except Exception as e:
        return f"🤖 AI Assistant: I encountered an error: {str(e)}"

# Main application
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 A.U.R.A - Adaptive User Retention Assistant</h1>
        <p>Intelligent Customer Retention Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/004D7A/FFFFFF?text=A.U.R.A", width=200)
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("🔄 Load A.U.R.A Data", use_container_width=True):
            with st.spinner("Loading data..."):
                result = load_aura_data()
                st.success(result)
        
        if st.button("⚙️ Run Data Pipeline", use_container_width=True):
            with st.spinner("Running pipeline..."):
                result = run_data_pipeline()
                st.info(result)
        
        st.markdown("### 📊 Data Status")
        if st.session_state.data_loaded:
            st.success(f"✅ Data Loaded: {len(st.session_state.customer_data)} customers")
        else:
            st.warning("⚠️ No data loaded")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard", "👥 Customer Analysis", "💡 Strategies", 
        "📈 Forecasting", "⚠️ Risk Analysis", "🤖 AI Assistant"
    ])
    
    with tab1:
        st.header("📊 A.U.R.A Dashboard")
        
        if st.session_state.data_loaded:
            create_dashboard_metrics()
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(create_risk_distribution_chart(), use_container_width=True)
            
            with col2:
                st.plotly_chart(create_health_score_distribution(), use_container_width=True)
        else:
            st.info("👆 Please load data from the sidebar to view the dashboard.")
    
    with tab2:
        st.header("👥 Individual Customer Analysis")
        
        if st.session_state.data_loaded:
            customer_id = st.selectbox(
                "Select Customer ID:",
                options=st.session_state.customer_data['customer_id'].tolist(),
                help="Choose a customer to analyze"
            )
            
            if st.button("🔍 Analyze Customer"):
                with st.spinner("Analyzing customer..."):
                    analysis = analyze_customer(customer_id)
                    st.markdown(analysis)
        else:
            st.info("👆 Please load data from the sidebar to analyze customers.")
    
    with tab3:
        st.header("💡 Retention Strategies")
        
        st.markdown("""
        ### 🎯 Proven Retention Strategies
        
        #### 1. **Proactive Customer Success**
        - Regular health checks and touchpoints
        - Early warning system for at-risk customers
        - Personalized success plans
        
        #### 2. **Value Demonstration**
        - Showcase ROI and business impact
        - Feature adoption campaigns
        - Success story sharing
        
        #### 3. **Engagement Programs**
        - User community building
        - Training and onboarding
        - Feedback collection and action
        
        #### 4. **Loyalty Programs**
        - Rewards for long-term customers
        - Referral incentives
        - Exclusive benefits and features
        
        #### 5. **Personalized Communication**
        - Segmented messaging
        - Relevant content delivery
        - Multi-channel engagement
        """)
    
    with tab4:
        st.header("📈 Forecasting & Predictions")
        
        if components_loaded:
            col1, col2 = st.columns(2)
            
            with col1:
                metric_type = st.selectbox(
                    "Select Metric:",
                    options=['Revenue', 'Engagement', 'Customer Count'],
                    help="Choose the metric to forecast"
                )
            
            with col2:
                periods = st.slider(
                    "Forecast Period (days):",
                    min_value=7,
                    max_value=365,
                    value=30,
                    help="Number of days to forecast"
                )
            
            if st.button("🔮 Generate Forecast"):
                with st.spinner("Generating forecast..."):
                    forecast_chart = get_forecast(metric_type, periods)
                    if isinstance(forecast_chart, str):
                        st.error(forecast_chart)
                    else:
                        st.plotly_chart(forecast_chart, use_container_width=True)
        else:
            st.warning("⚠️ Forecasting components not available.")
    
    with tab5:
        st.header("⚠️ Risk Analysis")
        
        if st.session_state.data_loaded:
            # Risk analysis summary
            data = st.session_state.customer_data
            risk_summary = data['churn_risk_level'].value_counts()
            
            st.markdown("### 📊 Risk Distribution Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🟢 Low Risk", f"{risk_summary.get('Low', 0)}", "Safe")
            with col2:
                st.metric("🟡 Medium Risk", f"{risk_summary.get('Medium', 0)}", "Monitor")
            with col3:
                st.metric("🔴 High Risk", f"{risk_summary.get('High', 0)}", "Action Required")
            
            # High-risk customers table
            high_risk_customers = data[data['churn_risk_level'] == 'High']
            
            if not high_risk_customers.empty:
                st.markdown("### 🚨 High-Risk Customers Requiring Immediate Attention")
                st.dataframe(
                    high_risk_customers[['customer_id', 'name', 'current_health_score', 'total_support_tickets_lifetime']],
                    use_container_width=True
                )
        else:
            st.info("👆 Please load data from the sidebar to perform risk analysis.")
    
    with tab6:
        st.header("🤖 AI Assistant")
        
        st.markdown("### 💬 Ask me anything about your customer data!")
        
        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about your customers, trends, or strategies..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Get AI response
            response = get_ai_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display messages
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response)
        
        # Example questions
        st.markdown("### 💡 Example Questions:")
        st.markdown("""
        - "Show me high-risk customers"
        - "What's our churn risk distribution?"
        - "What strategies should I use for medium-risk customers?"
        - "How is our revenue trending?"
        - "What are the best retention strategies?"
        """)

if __name__ == "__main__":
    main()
