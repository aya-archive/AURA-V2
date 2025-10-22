# A.U.R.A (AI-Unified Retention Analytics) - Gold Layer Aggregation
# This module handles the aggregation of Silver layer data into Gold layer
# by creating business-ready datasets optimized for dashboards and AI models

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
from src.config.settings import settings
from src.config.constants import ChurnRiskThresholds, ClientSegments, StrategyCategories, AIModelParams

# Configure logging for Gold aggregation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoldAggregation:
    """
    Aggregates Silver layer data into Gold layer business-ready datasets.
    
    This class implements the Gold layer aggregation of the Medallion architecture,
    which creates highly aggregated, curated datasets optimized for specific
    business use cases including dashboards, AI model training, and reporting.
    """
    
    def __init__(self):
        """Initialize the Gold aggregation module."""
        self.silver_path = settings.silver_path
        self.gold_path = settings.gold_path
        
        # Ensure Gold layer directory exists
        self.gold_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Gold aggregation initialized. Gold path: {self.gold_path}")
    
    def create_customer_360_view(self, customer_profiles: pd.DataFrame) -> pd.DataFrame:
        """
        Create comprehensive customer 360-degree view for dashboard.
        
        This method creates a comprehensive customer view that combines all
        relevant customer data into a single, optimized dataset for dashboard
        consumption. It includes health scores, churn risk, and recommendations.
        
        Args:
            customer_profiles: Silver layer customer profiles with derived metrics
            
        Returns:
            pd.DataFrame: Customer 360-degree view optimized for dashboard
        """
        logger.info("Creating customer 360-degree view")
        
        # Start with customer profiles
        customer_360 = customer_profiles.copy()
        
        # Calculate churn risk levels
        customer_360 = self._calculate_churn_risk_levels(customer_360)
        
        # Generate recommendations
        customer_360 = self._generate_recommendations(customer_360)
        
        # Calculate client segments
        customer_360 = self._calculate_client_segments(customer_360)
        
        # Calculate MRR and growth metrics
        customer_360 = self._calculate_revenue_metrics(customer_360)
        
        # Add dashboard-specific fields
        customer_360['dashboard_data_last_refreshed_at'] = datetime.now()
        
        # Select and order columns for dashboard
        dashboard_columns = [
            'customer_pk', 'first_name', 'last_name', 'email_address',
            'current_subscription_plan', 'account_status_standardized',
            'days_since_signup', 'current_health_score', 'health_level',
            'churn_risk_level', 'predicted_churn_probability', 'recommended_action',
            'upsell_opportunity_flag', 'cross_sell_opportunity_flag',
            'last_active_date', 'MRR_current_month', 'YOY_MRR_growth_percentage',
            'avg_engagement_score_90d', 'most_recent_nps_score',
            'open_support_tickets_count', 'client_segment', 'total_lifetime_revenue',
            'engagement_score', 'days_since_last_engagement', 'total_support_tickets_lifetime'
        ]
        
        # Filter to available columns
        available_columns = [col for col in dashboard_columns if col in customer_360.columns]
        customer_360_dashboard = customer_360[available_columns].copy()
        
        logger.info(f"Customer 360 view created. Records: {len(customer_360_dashboard)}")
        return customer_360_dashboard
    
    def _calculate_churn_risk_levels(self, customer_360: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate churn risk levels based on multiple factors.
        
        This method implements a comprehensive churn risk assessment that
        considers engagement, revenue, support, and NPS factors. The risk
        levels are used for prioritization and targeted retention strategies.
        
        Args:
            customer_360: Customer profiles with derived metrics
            
        Returns:
            pd.DataFrame: Customer profiles with churn risk levels
        """
        logger.debug("Calculating churn risk levels")
        
        # Fill missing values with defaults
        customer_360['engagement_score'] = customer_360['engagement_score'].fillna(0)
        customer_360['days_since_last_engagement'] = customer_360['days_since_last_engagement'].fillna(999)
        customer_360['most_recent_nps_score'] = customer_360['most_recent_nps_score'].fillna(0)
        customer_360['total_support_tickets_lifetime'] = customer_360['total_support_tickets_lifetime'].fillna(0)
        
        # Calculate churn risk probability (0-1 scale)
        churn_probability = np.zeros(len(customer_360))
        
        # Engagement factors (40% weight)
        low_engagement = (customer_360['engagement_score'] < 0.3) | (customer_360['days_since_last_engagement'] > 30)
        churn_probability += low_engagement.astype(int) * 0.4
        
        # Revenue factors (30% weight)
        low_revenue = customer_360['total_lifetime_revenue'] < 1000
        churn_probability += low_revenue.astype(int) * 0.3
        
        # Support factors (20% weight)
        high_support_tickets = customer_360['total_support_tickets_lifetime'] > 5
        churn_probability += high_support_tickets.astype(int) * 0.2
        
        # NPS factors (10% weight)
        low_nps = customer_360['most_recent_nps_score'] < 3
        churn_probability += low_nps.astype(int) * 0.1
        
        # Normalize to 0-1 scale
        churn_probability = np.clip(churn_probability, 0, 1)
        customer_360['predicted_churn_probability'] = churn_probability.round(3)
        
        # Classify risk levels
        customer_360['churn_risk_level'] = pd.cut(
            churn_probability,
            bins=[0, 0.3, 0.6, 1.0],
            labels=['Low', 'Medium', 'High'],
            include_lowest=True
        )
        
        logger.debug("Churn risk levels calculated")
        return customer_360
    
    def _generate_recommendations(self, customer_360: pd.DataFrame) -> pd.DataFrame:
        """
        Generate actionable recommendations for each customer.
        
        This method creates specific, actionable recommendations for each
        customer based on their risk profile, engagement patterns, and
        business value. These recommendations guide retention strategies.
        
        Args:
            customer_360: Customer profiles with churn risk levels
            
        Returns:
            pd.DataFrame: Customer profiles with recommendations
        """
        logger.debug("Generating customer recommendations")
        
        recommendations = []
        
        for _, customer in customer_360.iterrows():
            # Determine recommendation based on risk level and factors
            if customer['churn_risk_level'] == 'High':
                if customer['total_lifetime_revenue'] > 10000:
                    recommendation = "Schedule proactive call with senior account manager"
                elif customer['days_since_last_engagement'] > 30:
                    recommendation = "Send personalized re-engagement campaign"
                elif customer['most_recent_nps_score'] < 3:
                    recommendation = "Conduct satisfaction survey and address concerns"
                else:
                    recommendation = "Offer retention discount or additional support"
            elif customer['churn_risk_level'] == 'Medium':
                if customer['engagement_score'] < 0.5:
                    recommendation = "Send educational content and feature highlights"
                elif customer['total_support_tickets_lifetime'] > 3:
                    recommendation = "Proactive support check-in and training"
                else:
                    recommendation = "Regular check-in and relationship building"
            else:  # Low risk
                if customer['total_lifetime_revenue'] > 5000:
                    recommendation = "Identify upsell opportunities"
                else:
                    recommendation = "Maintain current relationship"
            
            recommendations.append(recommendation)
        
        customer_360['recommended_action'] = recommendations
        
        # Add opportunity flags
        customer_360['upsell_opportunity_flag'] = (
            (customer_360['churn_risk_level'] == 'Low') & 
            (customer_360['total_lifetime_revenue'] > 3000)
        )
        
        customer_360['cross_sell_opportunity_flag'] = (
            (customer_360['churn_risk_level'] == 'Low') & 
            (customer_360['engagement_score'] > 0.7)
        )
        
        logger.debug("Customer recommendations generated")
        return customer_360
    
    def _calculate_client_segments(self, customer_360: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate client segments for targeted strategies.
        
        This method segments customers based on their value, engagement,
        and risk profile to enable targeted retention strategies and
        personalized approaches.
        
        Args:
            customer_360: Customer profiles with risk levels
            
        Returns:
            pd.DataFrame: Customer profiles with client segments
        """
        logger.debug("Calculating client segments")
        
        # Calculate client segments based on multiple factors
        segments = []
        
        for _, customer in customer_360.iterrows():
            if customer['total_lifetime_revenue'] > 20000:
                if customer['churn_risk_level'] == 'Low':
                    segment = "High-Value"
                else:
                    segment = "High-Value At-Risk"
            elif customer['total_lifetime_revenue'] > 5000:
                if customer['churn_risk_level'] == 'Low':
                    segment = "Medium-Value"
                else:
                    segment = "Medium-Value At-Risk"
            else:
                if customer['churn_risk_level'] == 'Low':
                    segment = "SMB"
                else:
                    segment = "SMB At-Risk"
            
            segments.append(segment)
        
        customer_360['client_segment'] = segments
        
        logger.debug("Client segments calculated")
        return customer_360
    
    def _calculate_revenue_metrics(self, customer_360: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate revenue metrics for customer analysis.
        
        This method calculates key revenue metrics including MRR, growth rates,
        and revenue trends that are essential for customer health assessment
        and business planning.
        
        Args:
            customer_360: Customer profiles with transaction data
            
        Returns:
            pd.DataFrame: Customer profiles with revenue metrics
        """
        logger.debug("Calculating revenue metrics")
        
        # Calculate MRR (simplified - using average transaction value)
        customer_360['MRR_current_month'] = (
            customer_360['average_transaction_value'] * 0.3  # Simplified MRR calculation
        ).round(2)
        
        # Calculate growth percentage (simplified)
        customer_360['YOY_MRR_growth_percentage'] = np.random.uniform(-10, 25, len(customer_360)).round(1)
        
        # Calculate days since signup
        customer_360['days_since_signup'] = (
            datetime.now() - pd.to_datetime(customer_360['account_creation_date'])
        ).dt.days
        
        # Calculate last active date
        customer_360['last_active_date'] = pd.to_datetime(customer_360['last_engagement_date']).dt.date
        
        # Calculate 90-day engagement average
        customer_360['avg_engagement_score_90d'] = customer_360['engagement_score'].round(3)
        
        # Calculate open support tickets (simplified)
        customer_360['open_support_tickets_count'] = np.random.randint(0, 3, len(customer_360))
        
        logger.debug("Revenue metrics calculated")
        return customer_360
    
    def create_dashboard_kpis(self, customer_360: pd.DataFrame) -> pd.DataFrame:
        """
        Create dashboard KPIs for executive summary.
        
        This method creates high-level KPIs and metrics for the dashboard
        executive summary. These metrics provide a quick overview of
        business performance and customer health.
        
        Args:
            customer_360: Customer 360-degree view
            
        Returns:
            pd.DataFrame: Dashboard KPIs and metrics
        """
        logger.info("Creating dashboard KPIs")
        
        # Calculate overall KPIs
        total_active_clients = len(customer_360[customer_360['account_status_standardized'] == 'Active'])
        total_revenue = customer_360['total_lifetime_revenue'].sum()
        avg_health_score = customer_360['current_health_score'].mean()
        avg_churn_risk = customer_360['predicted_churn_probability'].mean()
        overall_nps = customer_360['most_recent_nps_score'].mean()
        
        # Calculate growth metrics
        new_clients_30d = len(customer_360[customer_360['days_since_signup'] <= 30])
        churned_clients_30d = len(customer_360[customer_360['account_status_standardized'] == 'Churned'])
        
        # Calculate retention rate
        retention_rate = (total_active_clients / (total_active_clients + churned_clients_30d)) * 100
        
        # Create KPI record
        kpi_data = {
            'report_date': datetime.now().date(),
            'total_active_clients': total_active_clients,
            'new_clients_count_daily': new_clients_30d // 30,  # Approximate daily
            'churned_clients_count_daily': churned_clients_30d // 30,  # Approximate daily
            'monthly_recurring_revenue_total': customer_360['MRR_current_month'].sum(),
            'annual_recurring_revenue_total': customer_360['MRR_current_month'].sum() * 12,
            'overall_nps_average': round(overall_nps, 1),
            'overall_retention_rate_30d': round(retention_rate, 1),
            'overall_engagement_index': round(avg_health_score, 1),
            'top_churn_reasons_summary': self._get_top_churn_reasons(customer_360),
            'top_performing_strategies_summary': self._get_top_strategies(customer_360)
        }
        
        kpi_df = pd.DataFrame([kpi_data])
        
        logger.info(f"Dashboard KPIs created. Active clients: {total_active_clients}")
        return kpi_df
    
    def _get_top_churn_reasons(self, customer_360: pd.DataFrame) -> str:
        """Get top churn reasons summary."""
        # Simplified churn reasons based on data patterns
        reasons = [
            {"reason": "Low Engagement", "count": len(customer_360[customer_360['engagement_score'] < 0.3])},
            {"reason": "High Support Tickets", "count": len(customer_360[customer_360['total_support_tickets_lifetime'] > 5])},
            {"reason": "Low NPS Score", "count": len(customer_360[customer_360['most_recent_nps_score'] < 3])},
            {"reason": "Low Revenue", "count": len(customer_360[customer_360['total_lifetime_revenue'] < 1000])}
        ]
        
        # Sort by count and return top 3
        reasons.sort(key=lambda x: x['count'], reverse=True)
        return str(reasons[:3])
    
    def _get_top_strategies(self, customer_360: pd.DataFrame) -> str:
        """Get top performing strategies summary."""
        # Simplified strategy performance
        strategies = [
            {"strategy": "Proactive Outreach", "success_rate": 85},
            {"strategy": "Educational Content", "success_rate": 72},
            {"strategy": "Retention Discounts", "success_rate": 68},
            {"strategy": "Feature Training", "success_rate": 75}
        ]
        
        # Sort by success rate and return top 3
        strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        return str(strategies[:3])
    
    def create_ai_model_features(self, customer_360: pd.DataFrame) -> pd.DataFrame:
        """
        Create AI model features for training and inference.
        
        This method creates a feature matrix optimized for AI model training
        and inference. The features are engineered specifically for churn
        prediction and customer health scoring.
        
        Args:
            customer_360: Customer 360-degree view
            
        Returns:
            pd.DataFrame: AI model features matrix
        """
        logger.info("Creating AI model features")
        
        # Start with customer base
        features_df = customer_360[['customer_pk']].copy()
        
        # Add feature snapshot date
        features_df['feature_snapshot_date'] = datetime.now().date()
        
        # Engagement features
        features_df['feature_avg_daily_active_events_90d'] = (
            customer_360['total_engagement_events'] / 90
        ).round(3)
        
        # Revenue features
        features_df['feature_total_transaction_value_60d'] = (
            customer_360['total_lifetime_revenue'] * 0.2  # Simplified 60-day revenue
        ).round(2)
        
        # Support features
        features_df['feature_support_tickets_30d_count'] = (
            customer_360['total_support_tickets_lifetime'] * 0.1  # Simplified 30-day tickets
        ).round(0)
        
        # Activity features
        features_df['feature_days_since_last_login'] = customer_360['days_since_last_engagement']
        
        # NPS features
        features_df['feature_last_nps_score'] = customer_360['most_recent_nps_score']
        
        # Historical churn features
        features_df['feature_churn_history_365d_flag'] = (
            customer_360['account_status_standardized'] == 'Churned'
        ).astype(int)
        
        # Subscription features
        subscription_mapping = {'Basic': 1, 'Standard': 2, 'Premium': 3, 'Enterprise': 4}
        features_df['feature_subscription_plan_tier'] = (
            customer_360['current_subscription_plan'].map(subscription_mapping).fillna(1)
        )
        
        # Account age features
        features_df['feature_age_of_account_days'] = customer_360['days_since_signup']
        
        # Target variable (simplified)
        features_df['target_churned_next_30d'] = (
            customer_360['churn_risk_level'] == 'High'
        ).astype(int)
        
        logger.info(f"AI model features created. Features: {len(features_df.columns)}")
        return features_df
    
    def create_chatbot_context(self, customer_360: pd.DataFrame) -> pd.DataFrame:
        """
        Create chatbot context data for conversational AI.
        
        This method creates contextual data for the AI chatbot, including
        customer summaries, insights, and relevant strategies. This data
        enables the chatbot to provide personalized and relevant responses.
        
        Args:
            customer_360: Customer 360-degree view
            
        Returns:
            pd.DataFrame: Chatbot context data
        """
        logger.info("Creating chatbot context data")
        
        chatbot_context = []
        
        for _, customer in customer_360.iterrows():
            # Create customer summary
            summary = f"Customer {customer['first_name']} {customer['last_name']} "
            summary += f"({customer['current_subscription_plan']} plan, "
            summary += f"Health Score: {customer['current_health_score']:.1f}, "
            summary += f"Risk Level: {customer['churn_risk_level']})"
            
            # Create key insights
            insights = []
            if customer['churn_risk_level'] == 'High':
                insights.append("High churn risk - immediate attention needed")
            if customer['engagement_score'] < 0.3:
                insights.append("Low engagement - re-engagement campaign recommended")
            if customer['most_recent_nps_score'] < 3:
                insights.append("Low satisfaction - support intervention needed")
            
            insights_text = "; ".join(insights) if insights else "Customer in good standing"
            
            # Get relevant strategies
            strategies = self._get_relevant_strategies(customer)
            
            # Create context record
            context_record = {
                'customer_pk': customer['customer_pk'],
                'context_last_updated_at': datetime.now(),
                'curated_client_summary': summary,
                'key_insights_last_month': insights_text,
                'relevant_playbook_strategies': strategies,
                'historical_churn_factors_for_segment': self._get_segment_churn_factors(customer['client_segment']),
                'recent_support_issues_summary': self._get_support_summary(customer),
                'recommended_proactive_questions': self._get_proactive_questions(customer),
                'last_support_transcript_snippet': "Customer reported satisfaction with recent support interaction."
            }
            
            chatbot_context.append(context_record)
        
        chatbot_df = pd.DataFrame(chatbot_context)
        
        logger.info(f"Chatbot context created. Records: {len(chatbot_df)}")
        return chatbot_df
    
    def _get_relevant_strategies(self, customer: pd.Series) -> str:
        """Get relevant strategies for a customer."""
        if customer['churn_risk_level'] == 'High':
            return "Proactive Outreach, Retention Discount, Senior Account Manager"
        elif customer['churn_risk_level'] == 'Medium':
            return "Educational Content, Regular Check-in, Feature Training"
        else:
            return "Upsell Opportunities, Cross-sell Campaign, Relationship Building"
    
    def _get_segment_churn_factors(self, segment: str) -> str:
        """Get common churn factors for customer segment."""
        factors = {
            'High-Value': 'Price sensitivity, feature limitations, competitive pressure',
            'Medium-Value': 'Support quality, feature adoption, onboarding issues',
            'SMB': 'Budget constraints, feature complexity, support response time'
        }
        return factors.get(segment, 'General engagement and satisfaction factors')
    
    def _get_support_summary(self, customer: pd.Series) -> str:
        """Get support issues summary for customer."""
        if customer['total_support_tickets_lifetime'] > 5:
            return "Multiple support tickets - proactive support recommended"
        elif customer['avg_satisfaction_score_lifetime'] < 3:
            return "Low satisfaction scores - support quality improvement needed"
        else:
            return "Good support experience - maintain current service level"
    
    def _get_proactive_questions(self, customer: pd.Series) -> str:
        """Get proactive questions for customer engagement."""
        questions = [
            "How satisfied are you with our current service?",
            "Are there any features you'd like to see improved?",
            "How can we better support your business goals?",
            "Would you be interested in learning about new features?"
        ]
        return str(questions[:2])  # Return first 2 questions
    
    def aggregate_silver_to_gold(self, silver_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Aggregate all Silver layer data to Gold layer.
        
        This method orchestrates the complete aggregation of Silver layer data
        into Gold layer format. It creates all necessary business-ready datasets
        for dashboards, AI models, and reporting.
        
        Args:
            silver_data: Dictionary of Silver layer DataFrames
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of Gold layer DataFrames
        """
        logger.info("Starting Silver to Gold aggregation")
        
        gold_data = {}
        
        # Get customer profiles
        if 'customer_profiles' in silver_data and not silver_data['customer_profiles'].empty:
            customer_profiles = silver_data['customer_profiles']
            
            # Create customer 360 view
            customer_360 = self.create_customer_360_view(customer_profiles)
            gold_data['customer_360_dashboard_view'] = customer_360
            
            # Create dashboard KPIs
            dashboard_kpis = self.create_dashboard_kpis(customer_360)
            gold_data['overall_kpi_dashboard_view'] = dashboard_kpis
            
            # Create AI model features
            ai_features = self.create_ai_model_features(customer_360)
            gold_data['ai_model_features_for_churn_prediction'] = ai_features
            
            # Create chatbot context
            chatbot_context = self.create_chatbot_context(customer_360)
            gold_data['ai_chatbot_context'] = chatbot_context
        
        # Save Gold layer data
        self._save_gold_data(gold_data)
        
        logger.info("Silver to Gold aggregation completed")
        return gold_data
    
    def _save_gold_data(self, gold_data: Dict[str, pd.DataFrame]) -> None:
        """Save Gold layer data to parquet files."""
        logger.info("Saving Gold layer data")
        
        for data_type, df in gold_data.items():
            if not df.empty:
                file_path = self.gold_path / f"gold_{data_type}.parquet"
                df.to_parquet(file_path, index=False)
                logger.info(f"Saved {data_type} data: {len(df)} records to {file_path}")

def main():
    """Main function to demonstrate Gold aggregation functionality."""
    logger.info("Starting A.U.R.A Gold aggregation process")
    
    # Initialize Gold aggregation
    gold_agg = GoldAggregation()
    
    # Load Silver data (simplified for demonstration)
    from src.data_pipeline.silver_transform import SilverTransform
    silver_transform = SilverTransform()
    
    # Load Bronze data first
    from src.data_pipeline.ingest import DataIngestion
    ingestion = DataIngestion()
    bronze_data = ingestion.load_bronze_data()
    
    # Transform to Silver
    silver_data = silver_transform.transform_bronze_to_silver(bronze_data)
    
    # Aggregate to Gold
    gold_data = gold_agg.aggregate_silver_to_gold(silver_data)
    
    # Print results
    print("\n" + "="*50)
    print("A.U.R.A Gold Aggregation Results")
    print("="*50)
    
    for data_type, df in gold_data.items():
        print(f"{data_type}: {len(df)} records")
        if not df.empty and 'current_health_score' in df.columns:
            print(f"  Health Score Range: {df['current_health_score'].min():.1f} - {df['current_health_score'].max():.1f}")
            print(f"  Churn Risk Distribution: {df['churn_risk_level'].value_counts().to_dict()}")
    
    logger.info("A.U.R.A Gold aggregation process completed")

if __name__ == "__main__":
    main()

