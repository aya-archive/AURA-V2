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

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.dashboard.utils.data_loader import DashboardDataLoader
from src.dashboard.utils.plot_utils import DashboardPlotUtils
from src.config.settings import settings

# Initialize A.U.R.A components
data_loader = DashboardDataLoader()
plot_utils = DashboardPlotUtils()

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
        print(f"Pipeline data not available: {e}")
    
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
        primary_hue=gr.themes.Color(c50="#e0eff7", c100="#c2e0f0", c200="#a3d0e9", c300="#85c1e2", c400="#66b1db", c500="#47a2d4", c600="#3a82a9", c700="#2d627e", c800="#204253", c900="#132228", c950="#0a1114"),
        secondary_hue=gr.themes.Color(c50="#e0f7f7", c100="#c2f0f0", c200="#a3e9e9", c300="#85e2e2", c400="#66dbdb", c500="#47d4d4", c600="#3aabab", c700="#2d8282", c800="#205353", c900="#132828", c950="#0a1414"),
        neutral_hue=gr.themes.Color(c50="#f8f8f8", c100="#f0f0f0", c200="#e9e9e9", c300="#e2e2e2", c400="#dbdbdb", c500="#d4d4d4", c600="#ababab", c700="#828282", c800="#535353", c900="#282828", c950="#141414"),
    ),
    css="""
    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    .gr-panel {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #004D7A;
        font-weight: 700;
    }
    .gr-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .gr-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    .gr-tab-button.selected {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
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
                status_text = gr.Textbox(label="Status", interactive=False)
            
            load_btn.click(
                load_aura_data,
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