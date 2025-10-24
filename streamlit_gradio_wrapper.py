# A.U.R.A (Adaptive User Retention Assistant) - Streamlit Wrapper for Gradio App
# This file runs the Gradio app within Streamlit Cloud environment

import streamlit as st
import subprocess
import sys
import os
import time
import threading
import requests
from pathlib import Path

# Configure Streamlit page
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
    .status-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #00B3B3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_gradio_server():
    """Check if Gradio server is running."""
    try:
        response = requests.get("http://localhost:7860", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_gradio_server():
    """Start the Gradio server in the background."""
    try:
        # Start the Gradio app
        process = subprocess.Popen([
            sys.executable, "aura_gradio_app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        st.error(f"Failed to start Gradio server: {e}")
        return None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 A.U.R.A - Adaptive User Retention Assistant</h1>
        <p>AI-Powered Customer Retention Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'gradio_started' not in st.session_state:
        st.session_state.gradio_started = False
    if 'gradio_process' not in st.session_state:
        st.session_state.gradio_process = None
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/004D7A/FFFFFF?text=A.U.R.A", width=200)
        st.markdown("### 🎯 AURA Platform Status")
        
        # Check if Gradio is running
        if check_gradio_server():
            st.success("✅ Gradio server is running")
            st.markdown("**🌐 Access your AURA platform:**")
            st.markdown("[Open AURA Dashboard](http://localhost:7860)")
        else:
            st.warning("⚠️ Gradio server not running")
            
        st.markdown("### 📊 Platform Features")
        st.markdown("""
        - **📊 Dashboard** - Real-time customer metrics
        - **👥 Customer Analysis** - Individual insights
        - **💡 Retention Strategies** - AI recommendations
        - **📈 Forecasting** - Predictive analytics
        - **⚠️ Risk Analysis** - Churn prediction
        - **🤖 AI Assistant** - Natural language queries
        """)
    
    # Main content
    st.markdown("## 🚀 AURA Platform Launcher")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🤖 About A.U.R.A
        
        **A.U.R.A (Adaptive User Retention Assistant)** is an AI-powered platform that transforms customer retention from reactive to proactive through intelligent analytics, automated insights, and actionable recommendations.
        
        #### 🎯 Key Features:
        - **AI-Powered Churn Prediction** - XGBoost models for accurate risk assessment
        - **Real-time Customer Health Monitoring** - Live dashboards with health scores
        - **Predictive Analytics** - Prophet forecasting for revenue and engagement trends
        - **Interactive Visualizations** - Dynamic charts and data exploration tools
        - **Natural Language AI Assistant** - Ask questions about your data in plain English
        - **Comprehensive Data Pipeline** - Bronze/Silver/Gold medallion architecture
        
        #### 🧠 AI Models Included:
        - **Prophet Forecasting** - Time series prediction for revenue and engagement
        - **Rule-based Decision Engine** - Churn risk classification and recommendations
        - **NLP Chatbot** - Intent recognition and natural language processing
        - **Sentiment Analysis** - Customer feedback and support ticket analysis
        """)
    
    with col2:
        st.markdown("### 🎮 Quick Actions")
        
        if st.button("🚀 Start AURA Platform", use_container_width=True):
            with st.spinner("Starting AURA platform..."):
                if not st.session_state.gradio_started:
                    process = start_gradio_server()
                    if process:
                        st.session_state.gradio_process = process
                        st.session_state.gradio_started = True
                        st.success("✅ AURA platform started successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to start AURA platform")
                else:
                    st.info("AURA platform is already running")
        
        if st.button("🔄 Restart Platform", use_container_width=True):
            if st.session_state.gradio_process:
                st.session_state.gradio_process.terminate()
                st.session_state.gradio_started = False
                st.session_state.gradio_process = None
            st.rerun()
        
        if st.button("📊 Open Dashboard", use_container_width=True):
            if check_gradio_server():
                st.markdown("**🌐 [Open AURA Dashboard](http://localhost:7860)**")
            else:
                st.warning("Please start the AURA platform first")
    
    # Status section
    st.markdown("### 📊 Platform Status")
    
    if check_gradio_server():
        st.markdown("""
        <div class="status-container">
            <h4>✅ AURA Platform is Running</h4>
            <p><strong>Status:</strong> Active and ready for use</p>
            <p><strong>URL:</strong> <a href="http://localhost:7860" target="_blank">http://localhost:7860</a></p>
            <p><strong>Features:</strong> All AI models loaded and ready</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Embed the Gradio app
        st.markdown("### 🎯 AURA Dashboard")
        st.markdown("**Click the link above to access the full AURA platform with all features:**")
        st.markdown("- 📊 Interactive Dashboard with real-time metrics")
        st.markdown("- 👥 Individual Customer Analysis and insights")
        st.markdown("- 💡 AI-Powered Retention Strategies")
        st.markdown("- 📈 Forecasting and Predictive Analytics")
        st.markdown("- ⚠️ Risk Analysis and Churn Prediction")
        st.markdown("- 🤖 Natural Language AI Assistant")
        
    else:
        st.markdown("""
        <div class="status-container">
            <h4>⚠️ AURA Platform Not Running</h4>
            <p><strong>Status:</strong> Please start the platform to access all features</p>
            <p><strong>Action:</strong> Click "Start AURA Platform" button above</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p><strong>🤖 A.U.R.A - Adaptive User Retention Assistant</strong></p>
        <p>Transforming customer retention through intelligent analytics</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
