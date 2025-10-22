# A.U.R.A (Adaptive User Retention Assistant) - Dashboard Data Loader
# This module provides data loading utilities for the Streamlit dashboard
# with caching and error handling for optimal performance

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
import streamlit as st
from src.config.settings import settings
from src.config.constants import Colors, TimePeriods

# Configure logging for data loader
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardDataLoader:
    """
    Data loader for A.U.R.A dashboard with caching and error handling.
    
    This class provides efficient data loading for the Streamlit dashboard
    with built-in caching, error handling, and data validation. It ensures
    optimal performance and reliability for the dashboard components.
    """
    
    def __init__(self):
        """Initialize the dashboard data loader."""
        self.gold_path = settings.gold_path
        self.silver_path = settings.silver_path
        self.bronze_path = settings.bronze_path
        
        logger.info("Dashboard data loader initialized")
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def load_customer_360_data(_self) -> pd.DataFrame:
        """
        Load customer 360-degree view data with caching.
        
        This method loads the customer 360-degree view data from the Gold layer
        with Streamlit caching for optimal performance. The data includes
        comprehensive customer profiles with health scores and recommendations.
        
        Returns:
            pd.DataFrame: Customer 360-degree view data
        """
        logger.info("Loading customer 360-degree view data")
        
        try:
            file_path = _self.gold_path / "gold_customer_360_dashboard_view.parquet"
            
            if file_path.exists():
                df = pd.read_parquet(file_path)
                logger.info(f"Loaded customer 360 data: {len(df)} records")
                return df
            else:
                logger.warning("Customer 360 data file not found, returning empty DataFrame")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error loading customer 360 data: {str(e)}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=300)
    def load_dashboard_kpis(_self) -> pd.DataFrame:
        """
        Load dashboard KPIs with caching.
        
        This method loads the dashboard KPIs from the Gold layer with caching
        for optimal performance. The KPIs provide high-level business metrics
        for the executive summary.
        
        Returns:
            pd.DataFrame: Dashboard KPIs data
        """
        logger.info("Loading dashboard KPIs")
        
        try:
            file_path = _self.gold_path / "gold_overall_kpi_dashboard_view.parquet"
            
            if file_path.exists():
                df = pd.read_parquet(file_path)
                logger.info(f"Loaded dashboard KPIs: {len(df)} records")
                return df
            else:
                logger.warning("Dashboard KPIs file not found, returning empty DataFrame")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error loading dashboard KPIs: {str(e)}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=300)
    def load_ai_model_features(_self) -> pd.DataFrame:
        """
        Load AI model features with caching.
        
        This method loads the AI model features from the Gold layer with caching
        for optimal performance. The features are used for model training and
        inference in the dashboard.
        
        Returns:
            pd.DataFrame: AI model features data
        """
        logger.info("Loading AI model features")
        
        try:
            file_path = _self.gold_path / "gold_ai_model_features_for_churn_prediction.parquet"
            
            if file_path.exists():
                df = pd.read_parquet(file_path)
                logger.info(f"Loaded AI model features: {len(df)} records")
                return df
            else:
                logger.warning("AI model features file not found, returning empty DataFrame")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error loading AI model features: {str(e)}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=300)
    def load_chatbot_context(_self) -> pd.DataFrame:
        """
        Load chatbot context data with caching.
        
        This method loads the chatbot context data from the Gold layer with caching
        for optimal performance. The context data enables personalized chatbot
        interactions and recommendations.
        
        Returns:
            pd.DataFrame: Chatbot context data
        """
        logger.info("Loading chatbot context data")
        
        try:
            file_path = _self.gold_path / "gold_ai_chatbot_context.parquet"
            
            if file_path.exists():
                df = pd.read_parquet(file_path)
                logger.info(f"Loaded chatbot context: {len(df)} records")
                return df
            else:
                logger.warning("Chatbot context file not found, returning empty DataFrame")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error loading chatbot context: {str(e)}")
            return pd.DataFrame()
    
    def load_silver_data(self, data_type: str) -> pd.DataFrame:
        """
        Load Silver layer data by type.
        
        This method loads specific Silver layer data types for detailed analysis
        and drill-down functionality in the dashboard.
        
        Args:
            data_type: Type of Silver layer data to load
            
        Returns:
            pd.DataFrame: Silver layer data
        """
        logger.info(f"Loading Silver layer data: {data_type}")
        
        try:
            file_path = self.silver_path / f"silver_{data_type}.parquet"
            
            if file_path.exists():
                df = pd.read_parquet(file_path)
                logger.info(f"Loaded Silver {data_type} data: {len(df)} records")
                return df
            else:
                logger.warning(f"Silver {data_type} data file not found")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error loading Silver {data_type} data: {str(e)}")
            return pd.DataFrame()
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get summary of available data.
        
        This method provides a summary of all available data sources
        for monitoring and debugging purposes.
        
        Returns:
            Dict[str, Any]: Data summary information
        """
        logger.info("Generating data summary")
        
        summary = {
            'gold_layer': {},
            'silver_layer': {},
            'bronze_layer': {},
            'last_updated': datetime.now()
        }
        
        # Check Gold layer files
        gold_files = [
            'customer_360_dashboard_view',
            'overall_kpi_dashboard_view',
            'ai_model_features_for_churn_prediction',
            'ai_chatbot_context'
        ]
        
        for file_name in gold_files:
            file_path = self.gold_path / f"gold_{file_name}.parquet"
            if file_path.exists():
                try:
                    df = pd.read_parquet(file_path)
                    summary['gold_layer'][file_name] = {
                        'records': len(df),
                        'columns': len(df.columns),
                        'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime)
                    }
                except Exception as e:
                    summary['gold_layer'][file_name] = {'error': str(e)}
        
        # Check Silver layer files
        silver_files = ['customers', 'transactions', 'engagement', 'support', 'surveys', 'customer_profiles']
        
        for file_name in silver_files:
            file_path = self.silver_path / f"silver_{file_name}.parquet"
            if file_path.exists():
                try:
                    df = pd.read_parquet(file_path)
                    summary['silver_layer'][file_name] = {
                        'records': len(df),
                        'columns': len(df.columns),
                        'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime)
                    }
                except Exception as e:
                    summary['silver_layer'][file_name] = {'error': str(e)}
        
        # Check Bronze layer files
        bronze_files = ['raw_customer_demographics', 'raw_transactions', 'raw_engagement_logs', 
                       'raw_support_interactions', 'raw_feedback_surveys']
        
        for file_name in bronze_files:
            file_path = self.bronze_path / f"{file_name}.csv"
            if file_path.exists():
                try:
                    df = pd.read_csv(file_path)
                    summary['bronze_layer'][file_name] = {
                        'records': len(df),
                        'columns': len(df.columns),
                        'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime)
                    }
                except Exception as e:
                    summary['bronze_layer'][file_name] = {'error': str(e)}
        
        logger.info("Data summary generated")
        return summary
    
    def filter_customer_data(self, df: pd.DataFrame, 
                           filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Filter customer data based on dashboard filters.
        
        This method applies dashboard filters to customer data for
        segmentation and analysis. It handles various filter types
        and ensures data consistency.
        
        Args:
            df: Customer data DataFrame
            filters: Dictionary of filter criteria
            
        Returns:
            pd.DataFrame: Filtered customer data
        """
        logger.info("Applying customer data filters")
        
        filtered_df = df.copy()
        
        # Apply risk level filter
        if 'risk_level' in filters and filters['risk_level']:
            filtered_df = filtered_df[filtered_df['churn_risk_level'].isin(filters['risk_level'])]
        
        # Apply client segment filter
        if 'client_segment' in filters and filters['client_segment']:
            filtered_df = filtered_df[filtered_df['client_segment'].isin(filters['client_segment'])]
        
        # Apply subscription plan filter
        if 'subscription_plan' in filters and filters['subscription_plan']:
            filtered_df = filtered_df[filtered_df['current_subscription_plan'].isin(filters['subscription_plan'])]
        
        # Apply health score range filter
        if 'health_score_min' in filters and filters['health_score_min'] is not None:
            filtered_df = filtered_df[filtered_df['current_health_score'] >= filters['health_score_min']]
        
        if 'health_score_max' in filters and filters['health_score_max'] is not None:
            filtered_df = filtered_df[filtered_df['current_health_score'] <= filters['health_score_max']]
        
        # Apply date range filter
        if 'date_range' in filters and filters['date_range']:
            start_date, end_date = filters['date_range']
            if 'last_active_date' in filtered_df.columns:
                filtered_df['last_active_date'] = pd.to_datetime(filtered_df['last_active_date'])
                filtered_df = filtered_df[
                    (filtered_df['last_active_date'] >= start_date) &
                    (filtered_df['last_active_date'] <= end_date)
                ]
        
        logger.info(f"Filtered customer data: {len(filtered_df)} records")
        return filtered_df
    
    def get_customer_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate customer insights from data.
        
        This method analyzes customer data to generate insights
        for the dashboard, including trends, patterns, and
        actionable recommendations.
        
        Args:
            df: Customer data DataFrame
            
        Returns:
            Dict[str, Any]: Customer insights and analytics
        """
        logger.info("Generating customer insights")
        
        if df.empty:
            return {'error': 'No data available for analysis'}
        
        insights = {
            'total_customers': len(df),
            'risk_distribution': df['churn_risk_level'].value_counts().to_dict(),
            'segment_distribution': df['client_segment'].value_counts().to_dict(),
            'subscription_distribution': df['current_subscription_plan'].value_counts().to_dict(),
            'average_health_score': df['current_health_score'].mean(),
            'high_risk_customers': len(df[df['churn_risk_level'] == 'High']),
            'critical_priority_customers': len(df[df['churn_risk_level'] == 'High']),
            'top_recommendations': df['recommended_action'].value_counts().head(5).to_dict()
        }
        
        # Calculate trends
        if 'current_health_score' in df.columns:
            insights['health_score_trend'] = {
                'min': df['current_health_score'].min(),
                'max': df['current_health_score'].max(),
                'median': df['current_health_score'].median(),
                'std': df['current_health_score'].std()
            }
        
        # Calculate revenue insights
        if 'total_lifetime_revenue' in df.columns:
            insights['revenue_insights'] = {
                'total_revenue': df['total_lifetime_revenue'].sum(),
                'average_revenue': df['total_lifetime_revenue'].mean(),
                'high_value_customers': len(df[df['total_lifetime_revenue'] > 10000])
            }
        
        # Generate alerts
        alerts = []
        if insights['high_risk_customers'] > 0:
            alerts.append(f"{insights['high_risk_customers']} customers are at high churn risk")
        
        if insights['average_health_score'] < 50:
            alerts.append("Overall customer health score is below 50")
        
        insights['alerts'] = alerts
        insights['generated_at'] = datetime.now()
        
        logger.info("Customer insights generated")
        return insights
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate data quality for dashboard display.
        
        This method performs data quality validation to ensure
        the dashboard displays accurate and reliable information.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dict[str, Any]: Data quality validation results
        """
        logger.info("Validating data quality")
        
        validation = {
            'total_records': len(df),
            'missing_values': {},
            'data_types': {},
            'quality_score': 0.0,
            'issues': [],
            'warnings': []
        }
        
        if df.empty:
            validation['issues'].append('Empty dataset')
            return validation
        
        # Check for missing values
        missing_values = df.isnull().sum()
        validation['missing_values'] = missing_values[missing_values > 0].to_dict()
        
        # Check data types
        validation['data_types'] = df.dtypes.to_dict()
        
        # Calculate quality score
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        quality_score = 1 - (missing_cells / total_cells)
        validation['quality_score'] = round(quality_score, 3)
        
        # Identify issues
        if quality_score < 0.8:
            validation['issues'].append('Low data quality score')
        
        if len(validation['missing_values']) > 0:
            validation['warnings'].append('Missing values detected')
        
        # Check for duplicate records
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            validation['warnings'].append(f'{duplicates} duplicate records found')
        
        logger.info(f"Data quality validation completed. Score: {quality_score:.3f}")
        return validation

def main():
    """Main function to demonstrate data loader functionality."""
    logger.info("Starting A.U.R.A dashboard data loader demonstration")
    
    # Initialize data loader
    data_loader = DashboardDataLoader()
    
    # Load data
    customer_data = data_loader.load_customer_360_data()
    kpis_data = data_loader.load_dashboard_kpis()
    
    # Generate summary
    summary = data_loader.get_data_summary()
    
    # Print results
    print("\n" + "="*50)
    print("A.U.R.A Dashboard Data Loader Results")
    print("="*50)
    print(f"Customer data: {len(customer_data)} records")
    print(f"KPIs data: {len(kpis_data)} records")
    
    print("\nData Summary:")
    for layer, files in summary.items():
        if layer != 'last_updated':
            print(f"  {layer}: {len(files)} files")
            for file_name, info in files.items():
                if 'records' in info:
                    print(f"    {file_name}: {info['records']} records")
    
    logger.info("A.U.R.A dashboard data loader demonstration completed")

if __name__ == "__main__":
    main()

