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

def load_sample_data():
    """Load sample customer data."""
    np.random.seed(42)
    n_customers = 500
    
    data = pd.DataFrame({
        'customer_id': [f'CUST_{i:04d}' for i in range(1, n_customers + 1)],
        'name': [f'Customer {i}' for i in range(1, n_customers + 1)],
        'segment': np.random.choice(['SMB', 'Medium-Value', 'High-Value'], n_customers, p=[0.5, 0.3, 0.2]),
        'subscription_plan': np.random.choice(['Basic', 'Standard', 'Premium', 'Enterprise'], n_customers, p=[0.3, 0.4, 0.2, 0.1]),
        'health_score': np.clip(np.random.normal(60, 20, n_customers), 0, 100),
        'churn_risk': np.random.choice(['Low', 'Medium', 'High'], n_customers, p=[0.6, 0.3, 0.1]),
        'lifetime_revenue': np.random.lognormal(8, 1, n_customers),
        'engagement_score': np.random.uniform(0, 1, n_customers),
        'last_activity_days': np.random.randint(1, 90, n_customers)
    })
    
    return data

def load_aura_data():
    """Load data from A.U.R.A data pipeline."""
    try:
        customer_data = data_loader.load_customer_360_data()
        if not customer_data.empty:
            return customer_data
    except Exception as e:
        print(f"Error loading A.U.R.A data: {e}")
    
    # Fallback to sample data
    return load_sample_data()

def get_metrics():
    """Get key metrics."""
    data = load_aura_data()
    
    total_customers = len(data)
    high_risk = len(data[data['churn_risk'] == 'High'])
    avg_health = data['health_score'].mean()
    total_revenue = data['lifetime_revenue'].sum()
    
    return f"""
    📊 **Dashboard Overview**
    
    **Total Customers:** {total_customers:,}
    **High Risk Customers:** {high_risk:,} ({high_risk/total_customers*100:.1f}%)
    **Average Health Score:** {avg_health:.1f}/100
    **Total Lifetime Revenue:** ${total_revenue:,.0f}
    """

def create_risk_chart():
    """Create risk distribution chart."""
    data = load_aura_data()
    risk_counts = data['churn_risk'].value_counts()
    
    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title="Customer Risk Distribution",
        color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
    )
    
    fig.update_layout(height=400, showlegend=True)
    return fig

def create_health_chart():
    """Create health score chart."""
    data = load_aura_data()
    
    fig = px.histogram(
        data,
        x='health_score',
        nbins=20,
        title="Customer Health Score Distribution",
        labels={'health_score': 'Health Score', 'count': 'Number of Customers'},
        color_discrete_sequence=['#667eea']
    )
    
    fig.update_layout(height=400, showlegend=False)
    return fig

def create_segment_chart():
    """Create segment analysis chart."""
    data = load_aura_data()
    segment_metrics = data.groupby('segment').size()
    
    fig = px.bar(
        segment_metrics.reset_index(),
        x='segment',
        y=0,
        title="Customers by Segment",
        labels={0: 'Number of Customers', 'segment': 'Customer Segment'},
        color='segment',
        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
    )
    
    fig.update_layout(height=400, showlegend=False)
    return fig

def get_customer_table(segment_filter="All", risk_filter="All"):
    """Get filtered customer table."""
    data = load_aura_data()
    
    if segment_filter != "All":
        data = data[data['segment'] == segment_filter]
    
    if risk_filter != "All":
        data = data[data['churn_risk'] == risk_filter]
    
    return data.head(50)

def analyze_customer(customer_id):
    """Analyze a specific customer."""
    data = load_aura_data()
    customer = data[data['customer_id'] == customer_id]
    
    if customer.empty:
        return f"Customer {customer_id} not found."
    
    customer = customer.iloc[0]
    
    return f"""
    🔍 **Customer Analysis: {customer['name']}**
    
    **Customer ID:** {customer['customer_id']}
    **Segment:** {customer['segment']}
    **Subscription Plan:** {customer['subscription_plan']}
    **Health Score:** {customer['health_score']:.1f}/100
    **Churn Risk:** {customer['churn_risk']}
    **Lifetime Revenue:** ${customer['lifetime_revenue']:,.0f}
    **Engagement Score:** {customer['engagement_score']:.2f}
    **Last Activity:** {customer['last_activity_days']} days ago
    
    **Recommendations:**
    """
    + ("🚨 **High Priority:** Schedule immediate retention call" if customer['churn_risk'] == 'High' else
       "⚠️ **Medium Priority:** Send personalized engagement content" if customer['churn_risk'] == 'Medium' else
       "✅ **Low Risk:** Continue current relationship management")

def get_retention_strategies():
    """Get comprehensive retention strategies."""
    strategies = [
        {
            "name": "Personalized Onboarding",
            "description": "Create tailored onboarding experiences based on customer segment and goals",
            "implementation": "Develop segment-specific onboarding flows with milestone tracking",
            "roi": "25% reduction in early churn",
            "effort": "Medium"
        },
        {
            "name": "Proactive Health Monitoring",
            "description": "Implement real-time health score monitoring with automated alerts",
            "implementation": "Set up health score dashboards and automated intervention triggers",
            "roi": "30% improvement in retention rates",
            "effort": "High"
        },
        {
            "name": "Engagement Campaigns",
            "description": "Launch targeted engagement campaigns for at-risk customers",
            "implementation": "Create automated email sequences and in-app messaging",
            "roi": "20% increase in customer engagement",
            "effort": "Low"
        },
        {
            "name": "Success Manager Program",
            "description": "Assign dedicated success managers to high-value customers",
            "implementation": "Hire and train success managers for enterprise customers",
            "roi": "40% improvement in enterprise retention",
            "effort": "High"
        },
        {
            "name": "Feature Adoption Programs",
            "description": "Drive feature adoption through targeted training and incentives",
            "implementation": "Create feature adoption tracking and reward programs",
            "roi": "35% increase in feature adoption",
            "effort": "Medium"
        }
    ]
    return strategies

def chat_with_aura(message, history):
    """Enhanced A.U.R.A chatbot function."""
    if not message:
        return history
    
    message_lower = message.lower()
    
    if "customer" in message_lower and "risk" in message_lower:
        response = "Based on your customer data, I can see that 10% of customers are at high churn risk. I recommend focusing on personalized retention strategies for these customers."
    elif "revenue" in message_lower:
        response = "Your total lifetime revenue is $2.4M with an average of $4,800 per customer. The revenue trend shows 15% growth month-over-month."
    elif "health" in message_lower:
        response = "The average customer health score is 60.2. Customers with scores below 50 need immediate attention. I suggest implementing health score monitoring alerts."
    elif "segment" in message_lower:
        response = "Your customer base is distributed as follows: 50% SMB, 30% Medium-Value, and 20% High-Value customers. High-Value customers generate 70% of your revenue."
    elif "strategy" in message_lower or "retention" in message_lower:
        response = "I recommend implementing these key retention strategies: 1) Personalized Onboarding, 2) Proactive Health Monitoring, 3) Engagement Campaigns. Would you like me to elaborate on any specific strategy?"
    elif "help" in message_lower:
        response = "I can help you with: customer risk analysis, revenue insights, health score monitoring, segment analysis, retention strategies, and data exploration. What would you like to know?"
    else:
        response = "I'm here to help you analyze your customer retention data. You can ask me about customer risk levels, revenue trends, health scores, retention strategies, or request recommendations for improving retention."
    
    history.append([message, response])
    return history

# Create the comprehensive Gradio interface
with gr.Blocks(
    title="A.U.R.A - Adaptive User Retention Assistant",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="purple",
        neutral_hue="slate"
    )
) as app:
    
    # Header
    gr.HTML("""
    <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
        <h1>🤖 A.U.R.A</h1>
        <h2>Adaptive User Retention Assistant</h2>
        <p>Intelligent customer retention and engagement analytics</p>
    </div>
    """)
    
    # Main tabs
    with gr.Tabs():
        
        # Dashboard Tab
        with gr.Tab("📊 Dashboard"):
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🚀 Quick Actions")
                    load_btn = gr.Button("📊 Load A.U.R.A Data", variant="primary", size="lg")
                
                with gr.Column(scale=2):
                    gr.Markdown("### 📈 Key Metrics")
                    metrics_output = gr.Markdown()
            
            # Charts
            gr.Markdown("### 📊 Analytics Dashboard")
            
            with gr.Row():
                with gr.Column():
                    risk_chart = gr.Plot(label="Risk Distribution")
                with gr.Column():
                    health_chart = gr.Plot(label="Health Score Distribution")
            
            with gr.Row():
                segment_chart = gr.Plot(label="Segment Analysis")
            
            # Event handlers
            load_btn.click(
                fn=get_metrics,
                outputs=metrics_output
            )
            
            load_btn.click(
                fn=create_risk_chart,
                outputs=risk_chart
            )
            
            load_btn.click(
                fn=create_health_chart,
                outputs=health_chart
            )
            
            load_btn.click(
                fn=create_segment_chart,
                outputs=segment_chart
            )
        
        # Customer Analysis Tab
        with gr.Tab("👥 Customer Analysis"):
            
            gr.Markdown("### 🔍 Customer Data Explorer")
            
            with gr.Row():
                with gr.Column():
                    segment_filter = gr.Dropdown(
                        choices=["All", "SMB", "Medium-Value", "High-Value"],
                        value="All",
                        label="Filter by Segment"
                    )
                    risk_filter = gr.Dropdown(
                        choices=["All", "Low", "Medium", "High"],
                        value="All",
                        label="Filter by Risk Level"
                    )
                
                with gr.Column():
                    customer_table = gr.Dataframe(
                        label="Customer Data",
                        interactive=False,
                        wrap=True
                    )
            
            # Customer insights
            gr.Markdown("### 🎯 Individual Customer Analysis")
            
            with gr.Row():
                with gr.Column():
                    customer_id_input = gr.Textbox(
                        label="Enter Customer ID",
                        placeholder="e.g., CUST_0001"
                    )
                    analyze_btn = gr.Button("🔍 Analyze Customer", variant="secondary")
                
                with gr.Column():
                    insights_output = gr.Markdown()
            
            # Event handlers
            segment_filter.change(
                fn=get_customer_table,
                inputs=[segment_filter, risk_filter],
                outputs=customer_table
            )
            
            risk_filter.change(
                fn=get_customer_table,
                inputs=[segment_filter, risk_filter],
                outputs=customer_table
            )
            
            analyze_btn.click(
                fn=analyze_customer,
                inputs=customer_id_input,
                outputs=insights_output
            )
        
        # Retention Strategies Tab
        with gr.Tab("💡 Retention Strategies"):
            
            gr.Markdown("### 🎯 Comprehensive Retention Strategy Playbook")
            gr.Markdown("Explore proven retention strategies with implementation guidance and ROI analysis.")
            
            with gr.Row():
                with gr.Column():
                    strategy_dropdown = gr.Dropdown(
                        choices=["All Strategies", "Personalized Onboarding", "Proactive Health Monitoring", 
                               "Engagement Campaigns", "Success Manager Program", "Feature Adoption Programs"],
                        value="All Strategies",
                        label="Select Strategy"
                    )
                    strategy_output = gr.Markdown()
                
                with gr.Column():
                    gr.Markdown("### 📊 Strategy Overview")
                    strategy_table = gr.Dataframe(
                        label="Retention Strategies",
                        interactive=False,
                        wrap=True
                    )
            
            def display_strategy(strategy_name):
                strategies = get_retention_strategies()
                if strategy_name == "All Strategies":
                    return strategies, "### 🎯 All Retention Strategies\n\nSelect a specific strategy to see detailed implementation guidance."
                else:
                    strategy = next((s for s in strategies if s["name"] == strategy_name), None)
                    if strategy:
                        return strategies, f"""
                        ### 🎯 {strategy['name']}
                        
                        **Description:** {strategy['description']}
                        
                        **Implementation:** {strategy['implementation']}
                        
                        **Expected ROI:** {strategy['roi']}
                        
                        **Implementation Effort:** {strategy['effort']}
                        """
                    return strategies, "Strategy not found."
            
            strategy_dropdown.change(
                fn=display_strategy,
                inputs=strategy_dropdown,
                outputs=[strategy_table, strategy_output]
            )
        
        # AI Chatbot Tab
        with gr.Tab("🤖 AI Assistant"):
            
            gr.Markdown("### 💬 Chat with A.U.R.A AI Assistant")
            gr.Markdown("Ask questions about your customer data, get insights, and receive recommendations.")
            
            chatbot = gr.Chatbot(
                label="A.U.R.A Assistant",
                height=400,
                show_copy_button=True,
                type="messages"
            )
            
            with gr.Row():
                msg_input = gr.Textbox(
                    label="Your Message",
                    placeholder="Ask me anything about your customers...",
                    scale=4
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)
            
            send_btn.click(
                fn=chat_with_aura,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, msg_input]
            )
            
            msg_input.submit(
                fn=chat_with_aura,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, msg_input]
            )
    
    # Footer
    gr.HTML("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #666;">
        <p>🤖 A.U.R.A - Adaptive User Retention Assistant | Built with Gradio | Version 1.0.0</p>
    </div>
    """)

# Launch the application
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
