# A.U.R.A (Adaptive User Retention Assistant) - Dashboard Plot Utilities
# This module provides visualization utilities for the Streamlit dashboard
# with consistent A.U.R.A branding and interactive charts

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
from src.config.constants import Colors, Typography

# Configure logging for plot utilities
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardPlotUtils:
    """
    Plot utilities for A.U.R.A dashboard with consistent branding.
    
    This class provides comprehensive visualization utilities for the Streamlit
    dashboard with consistent A.U.R.A branding, color schemes, and interactive
    features. All charts follow the A.U.R.A design guidelines.
    """
    
    def __init__(self):
        """Initialize the dashboard plot utilities."""
        self.colors = Colors()
        self.typography = Typography()
        
        # A.U.R.A color palette for charts
        self.color_palette = [
            self.colors.AURA_BLUE_DEEP,
            self.colors.AURA_TEAL,
            self.colors.AURA_ORANGE,
            self.colors.SUCCESS,
            self.colors.WARNING,
            self.colors.ERROR
        ]
        
        # Semantic colors for data visualization
        self.semantic_colors = {
            'success': self.colors.SUCCESS,
            'warning': self.colors.WARNING,
            'error': self.colors.ERROR,
            'info': self.colors.INFO,
            'primary': self.colors.AURA_BLUE_DEEP,
            'secondary': self.colors.AURA_TEAL
        }
        
        logger.info("Dashboard plot utilities initialized")
    
    def create_health_score_distribution(self, df: pd.DataFrame) -> go.Figure:
        """
        Create health score distribution chart.
        
        This method creates a histogram showing the distribution of customer
        health scores, helping identify overall customer health patterns
        and potential areas for improvement.
        
        Args:
            df: Customer data with health scores
            
        Returns:
            go.Figure: Interactive health score distribution chart
        """
        logger.info("Creating health score distribution chart")
        
        fig = go.Figure()
        
        # Create histogram
        fig.add_trace(go.Histogram(
            x=df['current_health_score'],
            nbinsx=20,
            marker_color=self.colors.AURA_BLUE_DEEP,
            opacity=0.7,
            name='Health Score Distribution'
        ))
        
        # Add mean line
        mean_score = df['current_health_score'].mean()
        fig.add_vline(
            x=mean_score,
            line_dash="dash",
            line_color=self.colors.AURA_TEAL,
            annotation_text=f"Mean: {mean_score:.1f}"
        )
        
        # Update layout
        fig.update_layout(
            title="Customer Health Score Distribution",
            xaxis_title="Health Score",
            yaxis_title="Number of Customers",
            template="plotly_white",
            font=dict(family=self.typography.FONT_FAMILY),
            showlegend=False
        )
        
        logger.info("Health score distribution chart created")
        return fig
    
    def create_risk_level_pie_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Create risk level pie chart.
        
        This method creates a pie chart showing the distribution of customer
        risk levels, providing a quick overview of the customer base
        risk profile.
        
        Args:
            df: Customer data with risk levels
            
        Returns:
            go.Figure: Interactive risk level pie chart
        """
        logger.info("Creating risk level pie chart")
        
        # Count risk levels
        risk_counts = df['churn_risk_level'].value_counts()
        
        # Define colors for risk levels
        risk_colors = {
            'Low': self.colors.SUCCESS,
            'Medium': self.colors.WARNING,
            'High': self.colors.ERROR
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=risk_counts.index,
            values=risk_counts.values,
            marker_colors=[risk_colors.get(level, self.colors.AURA_BLUE_DEEP) for level in risk_counts.index],
            textinfo='label+percent',
            textfont_size=12
        )])
        
        # Update layout
        fig.update_layout(
            title="Customer Risk Level Distribution",
            template="plotly_white",
            font=dict(family=self.typography.FONT_FAMILY),
            showlegend=True
        )
        
        logger.info("Risk level pie chart created")
        return fig
    
    def create_engagement_trend_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Create engagement trend chart.
        
        This method creates a line chart showing engagement trends over time,
        helping identify patterns and changes in customer engagement levels.
        
        Args:
            df: Customer data with engagement metrics
            
        Returns:
            go.Figure: Interactive engagement trend chart
        """
        logger.info("Creating engagement trend chart")
        
        # Group by date and calculate average engagement
        if 'last_engagement_date' in df.columns:
            df['last_engagement_date'] = pd.to_datetime(df['last_engagement_date'])
            engagement_trend = df.groupby(df['last_engagement_date'].dt.date)['engagement_score'].mean().reset_index()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=engagement_trend['last_engagement_date'],
                y=engagement_trend['engagement_score'],
                mode='lines+markers',
                name='Average Engagement',
                line=dict(color=self.colors.AURA_TEAL, width=3),
                marker=dict(size=6)
            ))
            
            # Update layout
            fig.update_layout(
                title="Customer Engagement Trend",
                xaxis_title="Date",
                yaxis_title="Engagement Score",
                template="plotly_white",
                font=dict(family=self.typography.FONT_FAMILY),
                hovermode='x unified'
            )
        else:
            # Create empty chart if no engagement data
            fig = go.Figure()
            fig.add_annotation(
                text="No engagement data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        logger.info("Engagement trend chart created")
        return fig
    
    def create_revenue_analysis_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Create revenue analysis chart.
        
        This method creates a scatter plot showing the relationship between
        customer health scores and revenue, helping identify high-value
        customers and revenue patterns.
        
        Args:
            df: Customer data with revenue and health metrics
            
        Returns:
            go.Figure: Interactive revenue analysis chart
        """
        logger.info("Creating revenue analysis chart")
        
        fig = go.Figure()
        
        # Create scatter plot
        fig.add_trace(go.Scatter(
            x=df['current_health_score'],
            y=df['total_lifetime_revenue'],
            mode='markers',
            marker=dict(
                size=8,
                color=df['churn_risk_level'].map({
                    'Low': self.colors.SUCCESS,
                    'Medium': self.colors.WARNING,
                    'High': self.colors.ERROR
                }),
                opacity=0.7
            ),
            text=df['customer_pk'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Health Score: %{x:.1f}<br>' +
                         'Revenue: $%{y:,.0f}<br>' +
                         '<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title="Customer Health Score vs Revenue",
            xaxis_title="Health Score",
            yaxis_title="Total Lifetime Revenue ($)",
            template="plotly_white",
            font=dict(family=self.typography.FONT_FAMILY),
            hovermode='closest'
        )
        
        logger.info("Revenue analysis chart created")
        return fig
    
    def create_support_tickets_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Create support tickets analysis chart.
        
        This method creates a bar chart showing support ticket patterns
        by customer segment, helping identify support trends and
        potential issues.
        
        Args:
            df: Customer data with support metrics
            
        Returns:
            go.Figure: Interactive support tickets chart
        """
        logger.info("Creating support tickets chart")
        
        # Group by client segment and calculate average support tickets
        support_analysis = df.groupby('client_segment')['total_support_tickets_lifetime'].mean().reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=support_analysis['client_segment'],
            y=support_analysis['total_support_tickets_lifetime'],
            marker_color=self.colors.AURA_BLUE_DEEP,
            text=support_analysis['total_support_tickets_lifetime'].round(1),
            textposition='auto'
        ))
        
        # Update layout
        fig.update_layout(
            title="Average Support Tickets by Client Segment",
            xaxis_title="Client Segment",
            yaxis_title="Average Support Tickets",
            template="plotly_white",
            font=dict(family=self.typography.FONT_FAMILY)
        )
        
        logger.info("Support tickets chart created")
        return fig
    
    def create_nps_analysis_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Create NPS analysis chart.
        
        This method creates a histogram showing the distribution of NPS scores,
        helping understand customer satisfaction levels and identify
        promoters, passives, and detractors.
        
        Args:
            df: Customer data with NPS scores
            
        Returns:
            go.Figure: Interactive NPS analysis chart
        """
        logger.info("Creating NPS analysis chart")
        
        fig = go.Figure()
        
        # Create histogram
        fig.add_trace(go.Histogram(
            x=df['most_recent_nps_score'],
            nbinsx=11,  # 0-10 scale
            marker_color=self.colors.AURA_TEAL,
            opacity=0.7,
            name='NPS Score Distribution'
        ))
        
        # Add NPS category lines
        fig.add_vline(x=9, line_dash="dash", line_color=self.colors.SUCCESS, annotation_text="Promoters (9-10)")
        fig.add_vline(x=7, line_dash="dash", line_color=self.colors.WARNING, annotation_text="Passives (7-8)")
        fig.add_vline(x=6, line_dash="dash", line_color=self.colors.ERROR, annotation_text="Detractors (0-6)")
        
        # Update layout
        fig.update_layout(
            title="NPS Score Distribution",
            xaxis_title="NPS Score",
            yaxis_title="Number of Customers",
            template="plotly_white",
            font=dict(family=self.typography.FONT_FAMILY),
            showlegend=False
        )
        
        logger.info("NPS analysis chart created")
        return fig
    
    def create_kpi_dashboard(self, kpis_df: pd.DataFrame) -> go.Figure:
        """
        Create KPI dashboard with key metrics.
        
        This method creates a comprehensive KPI dashboard showing
        key business metrics in an easy-to-read format with
        visual indicators for performance.
        
        Args:
            kpis_df: KPI data DataFrame
            
        Returns:
            go.Figure: Interactive KPI dashboard
        """
        logger.info("Creating KPI dashboard")
        
        if kpis_df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="No KPI data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
        
        # Get latest KPI data
        latest_kpis = kpis_df.iloc[-1]
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Active Clients', 'MRR Growth', 'NPS Score', 'Retention Rate'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Active clients indicator
        fig.add_trace(go.Indicator(
            mode="number",
            value=latest_kpis.get('total_active_clients', 0),
            title={"text": "Active Clients"},
            number={'font': {'size': 40, 'color': self.colors.AURA_BLUE_DEEP}}
        ), row=1, col=1)
        
        # MRR growth indicator
        mrr_growth = latest_kpis.get('YOY_MRR_growth_percentage', 0)
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=mrr_growth,
            title={"text": "MRR Growth (%)"},
            number={'font': {'size': 40, 'color': self.colors.AURA_TEAL}},
            delta={'reference': 0, 'relative': False}
        ), row=1, col=2)
        
        # NPS score indicator
        nps_score = latest_kpis.get('overall_nps_average', 0)
        fig.add_trace(go.Indicator(
            mode="number",
            value=nps_score,
            title={"text": "NPS Score"},
            number={'font': {'size': 40, 'color': self.colors.SUCCESS}}
        ), row=2, col=1)
        
        # Retention rate indicator
        retention_rate = latest_kpis.get('overall_retention_rate_30d', 0)
        fig.add_trace(go.Indicator(
            mode="number",
            value=retention_rate,
            title={"text": "Retention Rate (%)"},
            number={'font': {'size': 40, 'color': self.colors.AURA_ORANGE}}
        ), row=2, col=2)
        
        # Update layout
        fig.update_layout(
            title="A.U.R.A Key Performance Indicators",
            template="plotly_white",
            font=dict(family=self.typography.FONT_FAMILY),
            height=400
        )
        
        logger.info("KPI dashboard created")
        return fig
    
    def create_customer_segment_analysis(self, df: pd.DataFrame) -> go.Figure:
        """
        Create customer segment analysis chart.
        
        This method creates a comprehensive analysis of customer segments,
        showing health scores, risk levels, and revenue by segment
        for targeted retention strategies.
        
        Args:
            df: Customer data with segment information
            
        Returns:
            go.Figure: Interactive segment analysis chart
        """
        logger.info("Creating customer segment analysis chart")
        
        # Group by segment and calculate metrics
        segment_analysis = df.groupby('client_segment').agg({
            'current_health_score': 'mean',
            'total_lifetime_revenue': 'sum',
            'churn_risk_level': lambda x: (x == 'High').sum()
        }).reset_index()
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Health Score by Segment', 'Revenue by Segment'),
            specs=[[{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Health score by segment
        fig.add_trace(go.Bar(
            x=segment_analysis['client_segment'],
            y=segment_analysis['current_health_score'],
            name='Health Score',
            marker_color=self.colors.AURA_BLUE_DEEP
        ), row=1, col=1)
        
        # Revenue by segment
        fig.add_trace(go.Bar(
            x=segment_analysis['client_segment'],
            y=segment_analysis['total_lifetime_revenue'],
            name='Revenue',
            marker_color=self.colors.AURA_TEAL
        ), row=1, col=2)
        
        # Update layout
        fig.update_layout(
            title="Customer Segment Analysis",
            template="plotly_white",
            font=dict(family=self.typography.FONT_FAMILY),
            showlegend=False
        )
        
        logger.info("Customer segment analysis chart created")
        return fig
    
    def create_forecast_chart(self, forecast_data: pd.DataFrame) -> go.Figure:
        """
        Create forecast visualization chart.
        
        This method creates a line chart showing historical data and
        future forecasts with confidence intervals, helping users
        understand trends and predictions.
        
        Args:
            forecast_data: Forecast data with historical and predicted values
            
        Returns:
            go.Figure: Interactive forecast chart
        """
        logger.info("Creating forecast chart")
        
        fig = go.Figure()
        
        # Add historical data
        if 'y' in forecast_data.columns:
            fig.add_trace(go.Scatter(
                x=forecast_data['ds'],
                y=forecast_data['y'],
                mode='lines',
                name='Historical Data',
                line=dict(color=self.colors.AURA_BLUE_DEEP, width=2)
            ))
        
        # Add forecast
        if 'yhat' in forecast_data.columns:
            fig.add_trace(go.Scatter(
                x=forecast_data['ds'],
                y=forecast_data['yhat'],
                mode='lines',
                name='Forecast',
                line=dict(color=self.colors.AURA_TEAL, width=2)
            ))
        
        # Add confidence interval
        if 'yhat_upper' in forecast_data.columns and 'yhat_lower' in forecast_data.columns:
            fig.add_trace(go.Scatter(
                x=forecast_data['ds'],
                y=forecast_data['yhat_upper'],
                mode='lines',
                name='Upper Bound',
                line=dict(color='rgba(0, 179, 179, 0.3)', width=0),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_data['ds'],
                y=forecast_data['yhat_lower'],
                mode='lines',
                name='Confidence Interval',
                fill='tonexty',
                fillcolor='rgba(0, 179, 179, 0.3)',
                line=dict(color='rgba(0, 179, 179, 0.3)', width=0)
            ))
        
        # Update layout
        fig.update_layout(
            title="A.U.R.A Forecast Analysis",
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_white",
            font=dict(family=self.typography.FONT_FAMILY),
            hovermode='x unified'
        )
        
        logger.info("Forecast chart created")
        return fig

def main():
    """Main function to demonstrate plot utilities functionality."""
    logger.info("Starting A.U.R.A dashboard plot utilities demonstration")
    
    # Initialize plot utilities
    plot_utils = DashboardPlotUtils()
    
    # Create sample data
    sample_data = pd.DataFrame({
        'current_health_score': np.random.normal(60, 20, 100),
        'churn_risk_level': np.random.choice(['Low', 'Medium', 'High'], 100, p=[0.6, 0.3, 0.1]),
        'client_segment': np.random.choice(['SMB', 'Medium-Value', 'High-Value'], 100, p=[0.5, 0.3, 0.2]),
        'total_lifetime_revenue': np.random.lognormal(8, 1, 100),
        'most_recent_nps_score': np.random.choice(range(0, 11), 100)
    })
    
    # Create charts
    health_chart = plot_utils.create_health_score_distribution(sample_data)
    risk_chart = plot_utils.create_risk_level_pie_chart(sample_data)
    revenue_chart = plot_utils.create_revenue_analysis_chart(sample_data)
    
    print("\n" + "="*50)
    print("A.U.R.A Dashboard Plot Utilities Results")
    print("="*50)
    print("Charts created successfully:")
    print("- Health score distribution chart")
    print("- Risk level pie chart")
    print("- Revenue analysis chart")
    print(f"Sample data: {len(sample_data)} records")
    
    logger.info("A.U.R.A dashboard plot utilities demonstration completed")

if __name__ == "__main__":
    main()

