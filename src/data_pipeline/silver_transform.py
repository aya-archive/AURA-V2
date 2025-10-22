# A.U.R.A (AI-Unified Retention Analytics) - Silver Layer Transformation
# This module handles the transformation of Bronze layer data into Silver layer
# by cleaning, standardizing, and enriching the data for consistent analysis

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
from src.config.settings import settings
from src.config.constants import ChurnRiskThresholds, ClientSegments, TimePeriods

# Configure logging for data transformation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SilverTransform:
    """
    Transforms Bronze layer data into Silver layer through cleaning and enrichment.
    
    This class implements the Silver layer transformation of the Medallion architecture,
    which involves data cleaning, standardization, deduplication, and initial enrichment.
    The Silver layer provides a clean, consistent foundation for Gold layer aggregations
    and AI model training.
    """
    
    def __init__(self):
        """Initialize the Silver transformation module."""
        self.bronze_path = settings.bronze_path
        self.silver_path = settings.silver_path
        
        # Ensure Silver layer directory exists
        self.silver_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Silver transformation initialized. Silver path: {self.silver_path}")
    
    def clean_customer_data(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize customer demographics data.
        
        This method performs comprehensive cleaning of customer data including
        standardization of categorical values, handling of missing data,
        and data type conversions. It ensures data consistency for downstream
        processing and analysis.
        
        Args:
            customers_df: Raw customer demographics DataFrame
            
        Returns:
            pd.DataFrame: Cleaned customer data with standardized formats
        """
        logger.info("Cleaning customer demographics data")
        
        df = customers_df.copy()
        
        # Standardize customer ID
        df['customer_pk'] = df['customer_id'].astype(str)
        
        # Clean and standardize names
        df['first_name'] = df['first_name'].str.strip().str.title()
        df['last_name'] = df['last_name'].str.strip().str.title()
        
        # Standardize email addresses
        df['email_address'] = df['email'].str.lower().str.strip()
        
        # Standardize gender values
        gender_mapping = {
            'M': 'Male', 'F': 'Female', 'm': 'Male', 'f': 'Female',
            'male': 'Male', 'female': 'Female', 'other': 'Other'
        }
        df['gender_standardized'] = df['gender'].map(gender_mapping).fillna('Unknown')
        
        # Create age groups
        df['age_group'] = pd.cut(
            df['age'], 
            bins=[0, 25, 35, 45, 55, 65, 100], 
            labels=['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
            include_lowest=True
        )
        
        # Standardize subscription plans
        subscription_mapping = {
            'enterprise': 'Enterprise', 'premium': 'Premium', 'standard': 'Standard', 'basic': 'Basic'
        }
        df['current_subscription_plan'] = df['subscription_type'].str.lower().map(subscription_mapping).fillna(df['subscription_type'])
        
        # Standardize account status
        status_mapping = {
            'active': 'Active', 'inactive': 'Inactive', 'churned': 'Churned', 'trial': 'Trial'
        }
        df['account_status_standardized'] = df['status'].str.lower().map(status_mapping).fillna(df['status'])
        
        # Convert date columns
        df['account_creation_date'] = pd.to_datetime(df['account_creation_date'], errors='coerce')
        
        # Add data processing timestamp
        df['data_last_processed_at'] = datetime.now()
        
        logger.info(f"Customer data cleaning completed. Records: {len(df)}")
        return df
    
    def clean_transaction_data(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize transaction data.
        
        This method cleans transaction data by standardizing formats, handling
        missing values, and ensuring data consistency. It also performs basic
        validation to identify potential data quality issues.
        
        Args:
            transactions_df: Raw transaction DataFrame
            
        Returns:
            pd.DataFrame: Cleaned transaction data
        """
        logger.info("Cleaning transaction data")
        
        df = transactions_df.copy()
        
        # Convert date columns
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
        
        # Clean and standardize amounts
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df['amount'] = df['amount'].fillna(0)
        
        # Standardize currency
        df['currency'] = df['currency'].str.upper().fillna('USD')
        
        # Standardize payment methods
        payment_mapping = {
            'credit card': 'Credit Card', 'paypal': 'PayPal', 'bank transfer': 'Bank Transfer',
            'invoice': 'Invoice', 'cash': 'Cash'
        }
        df['payment_method'] = df['payment_method'].str.lower().map(payment_mapping).fillna(df['payment_method'])
        
        # Standardize transaction types
        type_mapping = {
            'purchase': 'Purchase', 'subscription': 'Subscription Payment', 'refund': 'Refund',
            'upgrade': 'Upgrade', 'downgrade': 'Downgrade'
        }
        df['transaction_type'] = df['transaction_type'].str.lower().map(type_mapping).fillna(df['transaction_type'])
        
        # Clean product information
        df['product_name'] = df['product_name'].str.strip()
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1)
        
        # Add data processing timestamp
        df['data_last_processed_at'] = datetime.now()
        
        logger.info(f"Transaction data cleaning completed. Records: {len(df)}")
        return df
    
    def clean_engagement_data(self, engagement_df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize engagement event data.
        
        This method cleans engagement data by standardizing event types,
        handling timestamps, and ensuring data consistency. It also
        performs basic validation for engagement patterns.
        
        Args:
            engagement_df: Raw engagement events DataFrame
            
        Returns:
            pd.DataFrame: Cleaned engagement data
        """
        logger.info("Cleaning engagement events data")
        
        df = engagement_df.copy()
        
        # Convert timestamp columns
        df['event_timestamp'] = pd.to_datetime(df['event_timestamp'], errors='coerce')
        
        # Standardize event types
        event_type_mapping = {
            'page_view': 'page_view', 'button_click': 'button_click', 'feature_usage': 'feature_usage',
            'login': 'login', 'logout': 'logout', 'dashboard_view': 'dashboard_view',
            'report_generation': 'report_generation', 'api_call': 'api_call'
        }
        df['event_type'] = df['event_type'].str.lower().map(event_type_mapping).fillna(df['event_type'])
        
        # Standardize device types
        device_mapping = {
            'desktop': 'Desktop', 'mobile': 'Mobile', 'tablet': 'Tablet'
        }
        df['device_type'] = df['device_type'].str.title().map(device_mapping).fillna(df['device_type'])
        
        # Clean browser information
        df['browser'] = df['browser'].str.title()
        df['operating_system'] = df['operating_system'].str.title()
        
        # Clean page URLs
        df['page_url'] = df['page_url'].str.strip()
        
        # Add data processing timestamp
        df['data_last_processed_at'] = datetime.now()
        
        logger.info(f"Engagement data cleaning completed. Records: {len(df)}")
        return df
    
    def clean_support_data(self, support_df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize support interaction data.
        
        This method cleans support data by standardizing interaction types,
        handling timestamps, and ensuring data consistency. It also performs
        basic validation for support patterns.
        
        Args:
            support_df: Raw support interactions DataFrame
            
        Returns:
            pd.DataFrame: Cleaned support data
        """
        logger.info("Cleaning support interactions data")
        
        df = support_df.copy()
        
        # Convert timestamp columns
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        df['resolved_at'] = pd.to_datetime(df['resolved_at'], errors='coerce')
        
        # Standardize interaction types
        interaction_mapping = {
            'chat': 'Chat', 'email': 'Email', 'call': 'Call', 'self-service': 'Self-service'
        }
        df['interaction_type'] = df['interaction_type'].str.lower().map(interaction_mapping).fillna(df['interaction_type'])
        
        # Standardize issue types
        issue_mapping = {
            'bug report': 'Bug Report', 'feature request': 'Feature Request',
            'billing inquiry': 'Billing Inquiry', 'technical support': 'Technical Support',
            'account issue': 'Account Issue'
        }
        df['issue_type'] = df['issue_type'].str.lower().map(issue_mapping).fillna(df['issue_type'])
        
        # Standardize status values
        status_mapping = {
            'open': 'Open', 'in progress': 'In Progress', 'resolved': 'Resolved', 'closed': 'Closed'
        }
        df['status'] = df['status'].str.lower().map(status_mapping).fillna(df['status'])
        
        # Clean satisfaction scores
        df['satisfaction_score'] = pd.to_numeric(df['satisfaction_score'], errors='coerce')
        df['satisfaction_score'] = df['satisfaction_score'].fillna(0)
        
        # Clean transcript text
        df['transcript_text'] = df['transcript_text'].str.strip()
        
        # Add data processing timestamp
        df['data_last_processed_at'] = datetime.now()
        
        logger.info(f"Support data cleaning completed. Records: {len(df)}")
        return df
    
    def clean_survey_data(self, surveys_df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize survey feedback data.
        
        This method cleans survey data by standardizing NPS scores,
        handling timestamps, and ensuring data consistency. It also
        performs basic validation for survey patterns.
        
        Args:
            surveys_df: Raw survey feedback DataFrame
            
        Returns:
            pd.DataFrame: Cleaned survey data
        """
        logger.info("Cleaning survey feedback data")
        
        df = surveys_df.copy()
        
        # Convert timestamp columns
        df['response_date'] = pd.to_datetime(df['response_date'], errors='coerce')
        
        # Clean NPS scores
        df['nps_score'] = pd.to_numeric(df['nps_score'], errors='coerce')
        df['nps_score'] = df['nps_score'].fillna(0)
        
        # Standardize survey types
        survey_mapping = {
            'nps': 'NPS', 'product feedback': 'Product Feedback',
            'onboarding survey': 'Onboarding Survey', 'support satisfaction': 'Support Satisfaction'
        }
        df['survey_type'] = df['survey_type'].str.lower().map(survey_mapping).fillna(df['survey_type'])
        
        # Clean comments and responses
        df['comments'] = df['comments'].str.strip()
        df['response_text'] = df['response_text'].str.strip()
        df['question_text'] = df['question_text'].str.strip()
        
        # Add data processing timestamp
        df['data_last_processed_at'] = datetime.now()
        
        logger.info(f"Survey data cleaning completed. Records: {len(df)}")
        return df
    
    def calculate_derived_metrics(self, customers_df: pd.DataFrame, 
                                transactions_df: pd.DataFrame,
                                engagement_df: pd.DataFrame,
                                support_df: pd.DataFrame,
                                surveys_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate derived metrics for customer profiles.
        
        This method calculates comprehensive derived metrics that combine
        data from multiple sources to create enriched customer profiles.
        These metrics are essential for churn prediction and customer health scoring.
        
        Args:
            customers_df: Cleaned customer data
            transactions_df: Cleaned transaction data
            engagement_df: Cleaned engagement data
            support_df: Cleaned support data
            surveys_df: Cleaned survey data
            
        Returns:
            pd.DataFrame: Customer profiles with derived metrics
        """
        logger.info("Calculating derived metrics for customer profiles")
        
        # Start with customer base
        customer_profiles = customers_df.copy()
        
        # Calculate transaction metrics
        transaction_metrics = self._calculate_transaction_metrics(customers_df, transactions_df)
        customer_profiles = customer_profiles.merge(transaction_metrics, on='customer_pk', how='left')
        
        # Calculate engagement metrics
        engagement_metrics = self._calculate_engagement_metrics(customers_df, engagement_df)
        customer_profiles = customer_profiles.merge(engagement_metrics, on='customer_pk', how='left')
        
        # Calculate support metrics
        support_metrics = self._calculate_support_metrics(customers_df, support_df)
        customer_profiles = customer_profiles.merge(support_metrics, on='customer_pk', how='left')
        
        # Calculate survey metrics
        survey_metrics = self._calculate_survey_metrics(customers_df, surveys_df)
        customer_profiles = customer_profiles.merge(survey_metrics, on='customer_pk', how='left')
        
        # Calculate composite health score
        customer_profiles = self._calculate_health_score(customer_profiles)
        
        logger.info(f"Derived metrics calculation completed. Records: {len(customer_profiles)}")
        return customer_profiles
    
    def _calculate_transaction_metrics(self, customers_df: pd.DataFrame, 
                                     transactions_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate transaction-based metrics for customers."""
        logger.debug("Calculating transaction metrics")
        
        # Filter transactions for existing customers
        valid_customers = set(customers_df['customer_pk'])
        transactions_df = transactions_df[transactions_df['customer_id'].isin(valid_customers)]
        
        if transactions_df.empty:
            return pd.DataFrame({'customer_pk': customers_df['customer_pk']})
        
        # Calculate transaction metrics
        transaction_metrics = transactions_df.groupby('customer_id').agg({
            'amount': ['sum', 'mean', 'count'],
            'transaction_date': ['min', 'max']
        }).round(2)
        
        # Flatten column names
        transaction_metrics.columns = [
            'total_lifetime_revenue', 'average_transaction_value', 'total_transactions_count',
            'first_transaction_date', 'last_transaction_date'
        ]
        
        # Calculate days since last transaction
        transaction_metrics['days_since_last_transaction'] = (
            datetime.now() - pd.to_datetime(transaction_metrics['last_transaction_date'])
        ).dt.days
        
        # Reset index
        transaction_metrics = transaction_metrics.reset_index()
        transaction_metrics = transaction_metrics.rename(columns={'customer_id': 'customer_pk'})
        
        return transaction_metrics
    
    def _calculate_engagement_metrics(self, customers_df: pd.DataFrame, 
                                     engagement_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate engagement-based metrics for customers."""
        logger.debug("Calculating engagement metrics")
        
        # Filter engagement events for existing customers
        valid_customers = set(customers_df['customer_pk'])
        engagement_df = engagement_df[engagement_df['customer_id'].isin(valid_customers)]
        
        if engagement_df.empty:
            return pd.DataFrame({'customer_pk': customers_df['customer_pk']})
        
        # Calculate engagement metrics
        engagement_metrics = engagement_df.groupby('customer_id').agg({
            'event_timestamp': ['min', 'max', 'count'],
            'event_type': 'nunique',
            'session_id': 'nunique'
        })
        
        # Flatten column names
        engagement_metrics.columns = [
            'first_engagement_date', 'last_engagement_date', 'total_engagement_events',
            'unique_event_types', 'total_sessions'
        ]
        
        # Calculate days since last engagement
        engagement_metrics['days_since_last_engagement'] = (
            datetime.now() - pd.to_datetime(engagement_metrics['last_engagement_date'])
        ).dt.days
        
        # Calculate engagement score (events per month)
        engagement_metrics['engagement_score'] = (
            engagement_metrics['total_engagement_events'] / 
            (engagement_metrics['days_since_last_engagement'] / 30 + 1)
        ).round(3)
        
        # Reset index
        engagement_metrics = engagement_metrics.reset_index()
        engagement_metrics = engagement_metrics.rename(columns={'customer_id': 'customer_pk'})
        
        return engagement_metrics
    
    def _calculate_support_metrics(self, customers_df: pd.DataFrame, 
                                 support_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate support-based metrics for customers."""
        logger.debug("Calculating support metrics")
        
        # Filter support tickets for existing customers
        valid_customers = set(customers_df['customer_pk'])
        support_df = support_df[support_df['customer_id'].isin(valid_customers)]
        
        if support_df.empty:
            return pd.DataFrame({'customer_pk': customers_df['customer_pk']})
        
        # Calculate support metrics
        support_metrics = support_df.groupby('customer_id').agg({
            'ticket_id': 'count',
            'satisfaction_score': 'mean',
            'created_at': 'max'
        }).round(2)
        
        # Flatten column names
        support_metrics.columns = [
            'total_support_tickets_lifetime', 'avg_satisfaction_score_lifetime', 'last_support_ticket_date'
        ]
        
        # Calculate days since last support ticket
        support_metrics['days_since_last_support_ticket'] = (
            datetime.now() - pd.to_datetime(support_metrics['last_support_ticket_date'])
        ).dt.days
        
        # Reset index
        support_metrics = support_metrics.reset_index()
        support_metrics = support_metrics.rename(columns={'customer_id': 'customer_pk'})
        
        return support_metrics
    
    def _calculate_survey_metrics(self, customers_df: pd.DataFrame, 
                                surveys_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate survey-based metrics for customers."""
        logger.debug("Calculating survey metrics")
        
        # Filter surveys for existing customers
        valid_customers = set(customers_df['customer_pk'])
        surveys_df = surveys_df[surveys_df['customer_id'].isin(valid_customers)]
        
        if surveys_df.empty:
            return pd.DataFrame({'customer_pk': customers_df['customer_pk']})
        
        # Calculate survey metrics
        survey_metrics = surveys_df.groupby('customer_id').agg({
            'nps_score': ['mean', 'max'],
            'response_date': 'max'
        }).round(2)
        
        # Flatten column names
        survey_metrics.columns = [
            'avg_nps_score_lifetime', 'most_recent_nps_score', 'last_survey_response_date'
        ]
        
        # Calculate days since last survey
        survey_metrics['days_since_last_survey'] = (
            datetime.now() - pd.to_datetime(survey_metrics['last_survey_response_date'])
        ).dt.days
        
        # Reset index
        survey_metrics = survey_metrics.reset_index()
        survey_metrics = survey_metrics.rename(columns={'customer_id': 'customer_pk'})
        
        return survey_metrics
    
    def _calculate_health_score(self, customer_profiles: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate composite health score for customers.
        
        This method calculates a comprehensive health score that combines
        engagement, revenue, support, and NPS metrics. The health score
        is a key indicator for churn prediction and customer prioritization.
        
        Args:
            customer_profiles: Customer profiles with derived metrics
            
        Returns:
            pd.DataFrame: Customer profiles with health scores
        """
        logger.debug("Calculating composite health scores")
        
        # Fill missing values with defaults
        customer_profiles['engagement_score'] = customer_profiles['engagement_score'].fillna(0)
        customer_profiles['total_lifetime_revenue'] = customer_profiles['total_lifetime_revenue'].fillna(0)
        customer_profiles['avg_satisfaction_score_lifetime'] = customer_profiles['avg_satisfaction_score_lifetime'].fillna(0)
        customer_profiles['most_recent_nps_score'] = customer_profiles['most_recent_nps_score'].fillna(0)
        
        # Normalize metrics to 0-1 scale
        engagement_normalized = customer_profiles['engagement_score'] / customer_profiles['engagement_score'].max()
        revenue_normalized = customer_profiles['total_lifetime_revenue'] / customer_profiles['total_lifetime_revenue'].max()
        support_normalized = customer_profiles['avg_satisfaction_score_lifetime'] / 5.0  # 5-point scale
        nps_normalized = customer_profiles['most_recent_nps_score'] / 10.0  # 10-point scale
        
        # Calculate weighted health score
        health_score = (
            engagement_normalized * 0.4 +  # 40% weight for engagement
            revenue_normalized * 0.3 +    # 30% weight for revenue
            support_normalized * 0.2 +   # 20% weight for support
            nps_normalized * 0.1          # 10% weight for NPS
        ) * 100  # Scale to 0-100
        
        customer_profiles['current_health_score'] = health_score.round(1)
        
        # Classify health levels
        customer_profiles['health_level'] = pd.cut(
            customer_profiles['current_health_score'],
            bins=[0, 40, 60, 80, 100],
            labels=['Poor', 'Fair', 'Good', 'Excellent'],
            include_lowest=True
        )
        
        logger.debug("Health score calculation completed")
        return customer_profiles
    
    def transform_bronze_to_silver(self, bronze_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Transform all Bronze layer data to Silver layer.
        
        This method orchestrates the complete transformation of Bronze layer data
        into Silver layer format. It applies cleaning, standardization, and
        enrichment to create a consistent, high-quality dataset for analysis.
        
        Args:
            bronze_data: Dictionary of Bronze layer DataFrames
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of Silver layer DataFrames
        """
        logger.info("Starting Bronze to Silver transformation")
        
        silver_data = {}
        
        # Clean individual datasets
        if 'customers' in bronze_data and not bronze_data['customers'].empty:
            silver_data['customers'] = self.clean_customer_data(bronze_data['customers'])
        
        if 'transactions' in bronze_data and not bronze_data['transactions'].empty:
            silver_data['transactions'] = self.clean_transaction_data(bronze_data['transactions'])
        
        if 'engagement' in bronze_data and not bronze_data['engagement'].empty:
            silver_data['engagement'] = self.clean_engagement_data(bronze_data['engagement'])
        
        if 'support' in bronze_data and not bronze_data['support'].empty:
            silver_data['support'] = self.clean_support_data(bronze_data['support'])
        
        if 'surveys' in bronze_data and not bronze_data['surveys'].empty:
            silver_data['surveys'] = self.clean_survey_data(bronze_data['surveys'])
        
        # Calculate derived metrics and create enriched customer profiles
        if 'customers' in silver_data:
            customer_profiles = self.calculate_derived_metrics(
                silver_data['customers'],
                silver_data.get('transactions', pd.DataFrame()),
                silver_data.get('engagement', pd.DataFrame()),
                silver_data.get('support', pd.DataFrame()),
                silver_data.get('surveys', pd.DataFrame())
            )
            silver_data['customer_profiles'] = customer_profiles
        
        # Save Silver layer data
        self._save_silver_data(silver_data)
        
        logger.info("Bronze to Silver transformation completed")
        return silver_data
    
    def _save_silver_data(self, silver_data: Dict[str, pd.DataFrame]) -> None:
        """Save Silver layer data to parquet files."""
        logger.info("Saving Silver layer data")
        
        for data_type, df in silver_data.items():
            if not df.empty:
                file_path = self.silver_path / f"silver_{data_type}.parquet"
                df.to_parquet(file_path, index=False)
                logger.info(f"Saved {data_type} data: {len(df)} records to {file_path}")

def main():
    """Main function to demonstrate Silver transformation functionality."""
    logger.info("Starting A.U.R.A Silver transformation process")
    
    # Initialize Silver transformation
    silver_transform = SilverTransform()
    
    # Load Bronze data (simplified for demonstration)
    from src.data_pipeline.ingest import DataIngestion
    ingestion = DataIngestion()
    bronze_data = ingestion.load_bronze_data()
    
    # Transform to Silver layer
    silver_data = silver_transform.transform_bronze_to_silver(bronze_data)
    
    # Print results
    print("\n" + "="*50)
    print("A.U.R.A Silver Transformation Results")
    print("="*50)
    
    for data_type, df in silver_data.items():
        print(f"{data_type}: {len(df)} records")
        if not df.empty and 'current_health_score' in df.columns:
            print(f"  Health Score Range: {df['current_health_score'].min():.1f} - {df['current_health_score'].max():.1f}")
            print(f"  Average Health Score: {df['current_health_score'].mean():.1f}")
    
    logger.info("A.U.R.A Silver transformation process completed")

if __name__ == "__main__":
    main()

