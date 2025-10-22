# A.U.R.A (Adaptive User Retention Assistant) - Main Dashboard Application
# This is the main Streamlit application for the A.U.R.A platform

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.dashboard.utils.data_loader import DashboardDataLoader
from src.dashboard.utils.plot_utils import DashboardPlotUtils
from src.dashboard.utils.styling import AURAStyling
from src.dashboard.components.client_dashboard import ClientDashboard
from src.dashboard.components.retention_strategies import RetentionStrategies
from src.dashboard.components.chatbot_interface import ChatbotInterface
from src.config.settings import settings

class AURADashboard:
    """
    Main A.U.R.A dashboard application.
    
    This class orchestrates the complete A.U.R.A dashboard experience,
    including data loading, visualization, and user interaction.
    """
    
    def __init__(self):
        """Initialize the A.U.R.A dashboard application."""
        self.data_loader = DashboardDataLoader()
        self.plot_utils = DashboardPlotUtils()
        self.styling = AURAStyling()
        self.client_dashboard = ClientDashboard()
        self.retention_strategies = RetentionStrategies()
        self.chatbot_interface = ChatbotInterface()
        
        # Initialize session state
        if 'customer_data' not in st.session_state:
            st.session_state.customer_data = pd.DataFrame()
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
    
    def run(self):
        """Run the A.U.R.A dashboard application."""
        logger.info("Starting A.U.R.A dashboard application")
        
        # Apply custom styling
        self.styling.apply_custom_css()
        self.styling.add_javascript_enhancements()
        
        # Configure page
        st.set_page_config(
            page_title="A.U.R.A - Adaptive User Retention Assistant",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Render sidebar
        self._render_sidebar()
        
        # Render header
        self._render_header()
        
        # Render main content based on selected page
        page = st.session_state.get('selected_page', 'Dashboard')
        
        if page == 'Dashboard':
            self._render_dashboard_page()
        elif page == 'Client Dashboard':
            self._render_client_dashboard_page()
        elif page == 'Retention Strategies':
            self._render_retention_strategies_page()
        elif page == 'AI Chatbot':
            self._render_chatbot_page()
        elif page == 'Modern UI Demo':
            self._render_modern_ui_demo_page()
        
        # Render footer
        self._render_footer()
    
    def _render_sidebar(self):
        """Render the sidebar navigation."""
        logger.info("Rendering sidebar")
        
        with st.sidebar:
            st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=A.U.R.A", width=200)
            
            st.markdown("### 🤖 A.U.R.A Navigation")
            
            # Page selection
            pages = [
                "Dashboard",
                "Client Dashboard", 
                "Retention Strategies",
                "AI Chatbot",
                "Modern UI Demo"
            ]
            
            selected_page = st.selectbox(
                "Select Page",
                pages,
                index=pages.index(st.session_state.get('selected_page', 'Dashboard'))
            )
            
            st.session_state.selected_page = selected_page
            
            st.markdown("---")
            
            # Data loading section
            st.markdown("### 📊 Data Management")
            
            if st.button("🔄 Load A.U.R.A Data", type="primary"):
                self._load_data()
            
            if st.button("📊 Generate Sample Data"):
                self._generate_sample_data()
            
            if st.session_state.data_loaded:
                st.success("✅ Data loaded successfully!")
            else:
                st.warning("⚠️ No data loaded. Click 'Load A.U.R.A Data' or 'Generate Sample Data'")
            
            st.markdown("---")
            
            # Quick stats
            if st.session_state.data_loaded and not st.session_state.customer_data.empty:
                st.markdown("### 📈 Quick Stats")
                data = st.session_state.customer_data
                
                total_customers = len(data)
                high_risk = len(data[data.get('churn_risk_level', data.get('churn_risk', '')) == 'High'])
                avg_health = data.get('current_health_score', data.get('health_score', pd.Series([0]))).mean()
                
                st.metric("Total Customers", f"{total_customers:,}")
                st.metric("High Risk", f"{high_risk:,}")
                st.metric("Avg Health Score", f"{avg_health:.1f}")
    
    def _render_header(self):
        """Render the application header."""
        logger.info("Rendering header")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h1>🤖 A.U.R.A - Adaptive User Retention Assistant</h1>
                <p style="font-size: 1.2em; color: #666;">
                    <strong>Adaptive User Retention Assistant Platform</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_dashboard_page(self):
        """Render the main dashboard page."""
        logger.info("Rendering dashboard page")
        
        st.markdown("## 📊 Executive Dashboard")
        
        if not st.session_state.data_loaded or st.session_state.customer_data.empty:
            st.warning("Please load data first using the sidebar options.")
            return
        
        data = st.session_state.customer_data
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_customers = len(data)
            st.metric("Total Customers", f"{total_customers:,}")
        
        with col2:
            high_risk = len(data[data.get('churn_risk_level', data.get('churn_risk', '')) == 'High'])
            st.metric("High Risk Customers", f"{high_risk:,}")
        
        with col3:
            avg_health = data.get('current_health_score', data.get('health_score', pd.Series([0]))).mean()
            st.metric("Average Health Score", f"{avg_health:.1f}")
        
        with col4:
            total_revenue = data.get('total_lifetime_revenue', data.get('lifetime_revenue', pd.Series([0]))).sum()
            st.metric("Total Revenue", f"${total_revenue:,.0f}")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Risk Distribution")
            risk_data = data.get('churn_risk_level', data.get('churn_risk', ''))
            if not risk_data.empty:
                risk_counts = risk_data.value_counts()
                fig = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title="Customer Risk Distribution",
                    color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Health Score Distribution")
            health_data = data.get('current_health_score', data.get('health_score', pd.Series([0])))
            if not health_data.empty:
                fig = px.histogram(
                    data,
                    x=health_data.name,
                    nbins=20,
                    title="Health Score Distribution",
                    color_discrete_sequence=['#667eea']
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Customer table
        st.markdown("### 👥 Customer Overview")
        display_cols = ['customer_id', 'name', 'segment', 'subscription_plan', 'health_score', 'churn_risk']
        available_cols = [col for col in display_cols if col in data.columns]
        st.dataframe(data[available_cols].head(20), use_container_width=True)
    
    def _render_client_dashboard_page(self):
        """Render the client dashboard page."""
        logger.info("Rendering client dashboard page")
        
        st.markdown("## 👥 Client Dashboard")
        
        if not st.session_state.data_loaded or st.session_state.customer_data.empty:
            st.warning("Please load data first using the sidebar options.")
            return
        
        # Client dashboard component
        self.client_dashboard.render()
    
    def _render_retention_strategies_page(self):
        """Render the retention strategies page."""
        logger.info("Rendering retention strategies page")
        
        st.markdown("## 💡 Retention Strategies")
        
        # Retention strategies component
        self.retention_strategies.render()
    
    def _render_chatbot_page(self):
        """Render the AI chatbot page."""
        logger.info("Rendering chatbot page")
        
        st.markdown("## 🤖 AI Chatbot Interface")
        
        # Chatbot interface component
        self.chatbot_interface.render()
    
    def _render_modern_ui_demo_page(self):
        """Render the modern UI demo page."""
        logger.info("Rendering modern UI demo page")
        
        st.markdown("## 🎨 Modern UI Components Demo")
        
        # Modern UI components
        from src.dashboard.components.modern_ui import ModernUI
        modern_ui = ModernUI()
        modern_ui.render()
    
    def _render_footer(self):
        """Render the application footer."""
        st.markdown("---")
        st.markdown(
            f"<div style='text-align: center; color: {self.styling.colors.MEDIUM_GRAY};'>"
            f"🤖 A.U.R.A - Adaptive User Retention Assistant | "
            f"Built with Streamlit | "
            f"Version {settings.PROJECT_VERSION}"
            f"</div>",
            unsafe_allow_html=True
        )
    
    def _load_data(self):
        """Load customer data from Gold layer."""
        logger.info("Loading customer data")
        
        try:
            # Load customer data from Gold layer
            customer_data = self.data_loader.load_customer_360_data()
            
            if customer_data.empty:
                st.error("No customer data found. Please run the data pipeline first.")
                return
            
            st.session_state.customer_data = customer_data
            st.session_state.data_loaded = True
            st.success("Customer data loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading customer data: {e}")
            st.error(f"Error loading customer data: {e}")
    
    def _generate_sample_data(self):
        """Generate sample customer data."""
        logger.info("Generating sample data")
        
        try:
            # Generate sample data
            np.random.seed(42)
            n_customers = 500
            
            sample_data = pd.DataFrame({
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
            
            st.session_state.customer_data = sample_data
            st.session_state.data_loaded = True
            st.success("Sample data generated successfully!")
            
        except Exception as e:
            logger.error(f"Error generating sample data: {e}")
            st.error(f"Error generating sample data: {e}")

# Initialize logging
import logging
logger = logging.getLogger(__name__)

# Main execution
if __name__ == "__main__":
    # Create and run the dashboard
    dashboard = AURADashboard()
    dashboard.run()

