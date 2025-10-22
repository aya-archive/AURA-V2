# A.U.R.A (Adaptive User Retention Assistant) - Client Dashboard Component
# This module provides the client monitoring dashboard component
# with KPIs, tables, and interactive charts for customer analysis

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from src.dashboard.utils.plot_utils import DashboardPlotUtils
from src.config.constants import Colors, Typography

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClientDashboard:
    """
    Client monitoring dashboard component for A.U.R.A platform.
    
    This class provides comprehensive client monitoring functionality including
    KPIs, interactive tables, and visualizations for customer health analysis
    and retention strategy planning.
    """
    
    def __init__(self):
        """Initialize the client dashboard component."""
        self.plot_utils = DashboardPlotUtils()
        self.colors = Colors()
        
        logger.info("Client dashboard component initialized")
    
    def render_executive_summary(self, customer_data: pd.DataFrame) -> None:
        """
        Render executive summary with key KPIs.
        
        This method displays high-level KPIs and metrics in an executive
        summary format, providing quick insights into customer health
        and business performance.
        
        Args:
            customer_data: Customer data DataFrame
        """
        logger.info("Rendering executive summary")
        
        st.subheader("📊 Executive Summary")
        
        # Calculate key metrics
        total_customers = len(customer_data)
        avg_health_score = customer_data['current_health_score'].mean()
        high_risk_count = len(customer_data[customer_data['churn_risk_level'] == 'High'])
        high_risk_percentage = (high_risk_count / total_customers * 100) if total_customers > 0 else 0
        
        # Create metrics columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Customers",
                f"{total_customers:,}",
                delta=None
            )
        
        with col2:
            st.metric(
                "Average Health Score",
                f"{avg_health_score:.1f}",
                delta=f"{avg_health_score - 50:.1f} from baseline"
            )
        
        with col3:
            st.metric(
                "High Risk Customers",
                f"{high_risk_count:,}",
                delta=f"{high_risk_percentage:.1f}%"
            )
        
        with col4:
            # Calculate engagement trend (simplified)
            if 'engagement_score' in customer_data.columns:
                avg_engagement = customer_data['engagement_score'].mean()
                st.metric(
                    "Avg Engagement",
                    f"{avg_engagement:.2f}",
                    delta="+0.05 from last month"
                )
            else:
                st.metric("Active Customers", f"{total_customers:,}")
        
        # Health score distribution chart
        st.markdown("#### Health Score Distribution")
        health_chart = self.plot_utils.create_health_score_distribution(customer_data)
        st.plotly_chart(health_chart, use_container_width=True)
    
    def render_risk_analysis(self, customer_data: pd.DataFrame) -> None:
        """
        Render risk analysis section.
        
        This method displays comprehensive risk analysis including
        risk level distribution, key risk factors, and actionable
        insights for retention planning.
        
        Args:
            customer_data: Customer data DataFrame
        """
        logger.info("Rendering risk analysis")
        
        st.subheader("⚠️ Risk Analysis")
        
        # Risk level distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Risk Level Distribution")
            risk_chart = self.plot_utils.create_risk_level_pie_chart(customer_data)
            st.plotly_chart(risk_chart, use_container_width=True)
        
        with col2:
            st.markdown("#### Revenue vs Health Score")
            revenue_chart = self.plot_utils.create_revenue_analysis_chart(customer_data)
            st.plotly_chart(revenue_chart, use_container_width=True)
        
        # Risk insights
        st.markdown("#### Risk Insights")
        
        # Calculate risk insights
        risk_insights = self._calculate_risk_insights(customer_data)
        
        for insight in risk_insights:
            if insight['type'] == 'warning':
                st.warning(insight['message'])
            elif insight['type'] == 'info':
                st.info(insight['message'])
            else:
                st.success(insight['message'])
    
    def render_customer_table(self, customer_data: pd.DataFrame) -> None:
        """
        Render interactive customer table.
        
        This method displays a comprehensive customer table with
        sorting, filtering, and interactive features for detailed
        customer analysis and management.
        
        Args:
            customer_data: Customer data DataFrame
        """
        logger.info("Rendering customer table")
        
        st.subheader("👥 Customer Details")
        
        # Table filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_filter = st.selectbox(
                "Filter by Risk Level:",
                ["All"] + list(customer_data['churn_risk_level'].unique())
            )
        
        with col2:
            segment_filter = st.selectbox(
                "Filter by Segment:",
                ["All"] + list(customer_data['client_segment'].unique())
            )
        
        with col3:
            plan_filter = st.selectbox(
                "Filter by Plan:",
                ["All"] + list(customer_data['current_subscription_plan'].unique())
            )
        
        # Apply filters
        filtered_data = customer_data.copy()
        
        if risk_filter != "All":
            filtered_data = filtered_data[filtered_data['churn_risk_level'] == risk_filter]
        
        if segment_filter != "All":
            filtered_data = filtered_data[filtered_data['client_segment'] == segment_filter]
        
        if plan_filter != "All":
            filtered_data = filtered_data[filtered_data['current_subscription_plan'] == plan_filter]
        
        # Display table
        display_columns = [
            'customer_pk', 'first_name', 'last_name', 'current_subscription_plan',
            'current_health_score', 'churn_risk_level', 'recommended_action'
        ]
        
        available_columns = [col for col in display_columns if col in filtered_data.columns]
        table_data = filtered_data[available_columns].copy()
        
        # Format data for display
        if 'current_health_score' in table_data.columns:
            table_data['current_health_score'] = table_data['current_health_score'].round(1)
        
        # Add risk level styling
        def style_risk_level(val):
            if val == 'High':
                return f'background-color: {self.colors.ERROR}; color: white'
            elif val == 'Medium':
                return f'background-color: {self.colors.WARNING}; color: black'
            else:
                return f'background-color: {self.colors.SUCCESS}; color: white'
        
        # Display styled table
        styled_table = table_data.style.applymap(
            style_risk_level, 
            subset=['churn_risk_level']
        )
        
        st.dataframe(
            styled_table,
            use_container_width=True,
            height=400
        )
        
        # Table summary
        st.markdown(f"**Showing {len(table_data)} of {len(customer_data)} customers**")
        
        # Download button
        csv = table_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Customer Data",
            data=csv,
            file_name=f"aura_customers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    def render_customer_details(self, customer_data: pd.DataFrame) -> None:
        """
        Render detailed customer view.
        
        This method provides detailed customer information with
        drill-down capabilities for individual customer analysis
        and retention strategy planning.
        
        Args:
            customer_data: Customer data DataFrame
        """
        logger.info("Rendering customer details")
        
        st.subheader("🔍 Customer Details")
        
        # Customer selector
        customer_options = customer_data['customer_pk'].tolist()
        selected_customer = st.selectbox(
            "Select Customer:",
            customer_options
        )
        
        if selected_customer:
            customer_info = customer_data[customer_data['customer_pk'] == selected_customer].iloc[0]
            
            # Customer overview
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Customer Information")
                st.markdown(f"**Name:** {customer_info.get('first_name', 'N/A')} {customer_info.get('last_name', 'N/A')}")
                st.markdown(f"**Email:** {customer_info.get('email_address', 'N/A')}")
                st.markdown(f"**Plan:** {customer_info.get('current_subscription_plan', 'N/A')}")
                st.markdown(f"**Segment:** {customer_info.get('client_segment', 'N/A')}")
            
            with col2:
                st.markdown("#### Health Metrics")
                health_score = customer_info.get('current_health_score', 0)
                risk_level = customer_info.get('churn_risk_level', 'Unknown')
                
                # Health score gauge
                st.markdown(f"**Health Score:** {health_score:.1f}")
                st.progress(health_score / 100)
                
                # Risk level indicator
                risk_color = {
                    'High': self.colors.ERROR,
                    'Medium': self.colors.WARNING,
                    'Low': self.colors.SUCCESS
                }.get(risk_level, self.colors.MEDIUM_GRAY)
                
                st.markdown(f"**Risk Level:** <span style='color: {risk_color}; font-weight: bold;'>{risk_level}</span>", unsafe_allow_html=True)
            
            # Recommendations
            st.markdown("#### AI Recommendations")
            recommended_action = customer_info.get('recommended_action', 'No recommendations available')
            st.info(f"**Recommended Action:** {recommended_action}")
            
            # Additional metrics
            if 'total_lifetime_revenue' in customer_info:
                st.metric("Total Lifetime Revenue", f"${customer_info['total_lifetime_revenue']:,.2f}")
            
            if 'engagement_score' in customer_info:
                st.metric("Engagement Score", f"{customer_info['engagement_score']:.3f}")
            
            if 'most_recent_nps_score' in customer_info:
                st.metric("NPS Score", f"{customer_info['most_recent_nps_score']}")
    
    def render_engagement_analysis(self, customer_data: pd.DataFrame) -> None:
        """
        Render engagement analysis section.
        
        This method displays engagement trends, patterns, and insights
        to help understand customer engagement levels and identify
        opportunities for improvement.
        
        Args:
            customer_data: Customer data DataFrame
        """
        logger.info("Rendering engagement analysis")
        
        st.subheader("📈 Engagement Analysis")
        
        # Engagement metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'engagement_score' in customer_data.columns:
                avg_engagement = customer_data['engagement_score'].mean()
                st.metric("Average Engagement", f"{avg_engagement:.3f}")
        
        with col2:
            if 'days_since_last_engagement' in customer_data.columns:
                avg_days = customer_data['days_since_last_engagement'].mean()
                st.metric("Avg Days Since Engagement", f"{avg_days:.1f}")
        
        with col3:
            if 'total_engagement_events' in customer_data.columns:
                total_events = customer_data['total_engagement_events'].sum()
                st.metric("Total Engagement Events", f"{total_events:,}")
        
        # Engagement charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Engagement by Segment")
            if 'client_segment' in customer_data.columns and 'engagement_score' in customer_data.columns:
                segment_engagement = customer_data.groupby('client_segment')['engagement_score'].mean().reset_index()
                st.bar_chart(segment_engagement.set_index('client_segment'))
        
        with col2:
            st.markdown("#### Engagement vs Risk Level")
            if 'churn_risk_level' in customer_data.columns and 'engagement_score' in customer_data.columns:
                risk_engagement = customer_data.groupby('churn_risk_level')['engagement_score'].mean().reset_index()
                st.bar_chart(risk_engagement.set_index('churn_risk_level'))
    
    def render_revenue_analysis(self, customer_data: pd.DataFrame) -> None:
        """
        Render revenue analysis section.
        
        This method displays revenue metrics, trends, and insights
        to help understand customer value and revenue patterns
        for strategic planning.
        
        Args:
            customer_data: Customer data DataFrame
        """
        logger.info("Rendering revenue analysis")
        
        st.subheader("💰 Revenue Analysis")
        
        # Revenue metrics
        if 'total_lifetime_revenue' in customer_data.columns:
            total_revenue = customer_data['total_lifetime_revenue'].sum()
            avg_revenue = customer_data['total_lifetime_revenue'].mean()
            high_value_customers = len(customer_data[customer_data['total_lifetime_revenue'] > 10000])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Revenue", f"${total_revenue:,.2f}")
            
            with col2:
                st.metric("Average Revenue", f"${avg_revenue:,.2f}")
            
            with col3:
                st.metric("High Value Customers", f"{high_value_customers:,}")
            
            # Revenue distribution
            st.markdown("#### Revenue Distribution")
            revenue_chart = self.plot_utils.create_revenue_analysis_chart(customer_data)
            st.plotly_chart(revenue_chart, use_container_width=True)
    
    def _calculate_risk_insights(self, customer_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Calculate risk insights from customer data.
        
        This method analyzes customer data to generate actionable
        insights about risk patterns and recommendations.
        
        Args:
            customer_data: Customer data DataFrame
            
        Returns:
            List[Dict[str, Any]]: List of risk insights
        """
        insights = []
        
        # High risk customer count
        high_risk_count = len(customer_data[customer_data['churn_risk_level'] == 'High'])
        if high_risk_count > 0:
            insights.append({
                'type': 'warning',
                'message': f"{high_risk_count} customers are at high churn risk and require immediate attention."
            })
        
        # Low health score
        if 'current_health_score' in customer_data.columns:
            avg_health = customer_data['current_health_score'].mean()
            if avg_health < 50:
                insights.append({
                    'type': 'warning',
                    'message': f"Average health score is {avg_health:.1f}, which is below the recommended threshold of 50."
                })
        
        # Engagement issues
        if 'engagement_score' in customer_data.columns:
            low_engagement = len(customer_data[customer_data['engagement_score'] < 0.3])
            if low_engagement > 0:
                insights.append({
                    'type': 'info',
                    'message': f"{low_engagement} customers have low engagement scores and may benefit from re-engagement campaigns."
                })
        
        # Revenue opportunities
        if 'total_lifetime_revenue' in customer_data.columns:
            high_value_low_risk = len(customer_data[
                (customer_data['total_lifetime_revenue'] > 10000) & 
                (customer_data['churn_risk_level'] == 'Low')
            ])
            if high_value_low_risk > 0:
                insights.append({
                    'type': 'success',
                    'message': f"{high_value_low_risk} high-value customers are at low risk - consider upsell opportunities."
                })
        
        return insights

def main():
    """Main function to demonstrate client dashboard functionality."""
    logger.info("Starting A.U.R.A client dashboard demonstration")
    
    # Initialize client dashboard
    client_dashboard = ClientDashboard()
    
    # Create sample data
    sample_data = pd.DataFrame({
        'customer_pk': [f'CUST_{i:03d}' for i in range(1, 101)],
        'first_name': ['John', 'Jane', 'Mike', 'Sarah'] * 25,
        'last_name': ['Smith', 'Johnson', 'Williams', 'Brown'] * 25,
        'email_address': [f'customer{i}@company.com' for i in range(1, 101)],
        'current_subscription_plan': np.random.choice(['Basic', 'Standard', 'Premium', 'Enterprise'], 100),
        'current_health_score': np.random.normal(60, 20, 100),
        'churn_risk_level': np.random.choice(['Low', 'Medium', 'High'], 100, p=[0.6, 0.3, 0.1]),
        'client_segment': np.random.choice(['SMB', 'Medium-Value', 'High-Value'], 100, p=[0.5, 0.3, 0.2]),
        'recommended_action': np.random.choice([
            'Schedule proactive call',
            'Send educational content',
            'Offer retention discount',
            'Maintain current relationship'
        ], 100),
        'total_lifetime_revenue': np.random.lognormal(8, 1, 100),
        'engagement_score': np.random.uniform(0, 1, 100)
    })
    
    print("\n" + "="*50)
    print("A.U.R.A Client Dashboard Results")
    print("="*50)
    print(f"Sample data: {len(sample_data)} customers")
    print(f"Risk distribution: {sample_data['churn_risk_level'].value_counts().to_dict()}")
    print(f"Average health score: {sample_data['current_health_score'].mean():.1f}")
    
    logger.info("A.U.R.A client dashboard demonstration completed")

if __name__ == "__main__":
    main()