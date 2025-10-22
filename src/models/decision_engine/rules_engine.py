# A.U.R.A (AI-Unified Retention Analytics) - Rule-Based Decision Engine
# This module implements a rule-based decision engine for churn prediction
# and retention strategy recommendations in the A.U.R.A platform

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
from src.config.settings import settings
from src.config.constants import ChurnRiskThresholds, ClientSegments, StrategyCategories, AIModelParams

# Configure logging for decision engine
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RuleBasedDecisionEngine:
    """
    Rule-based decision engine for A.U.R.A platform.
    
    This class implements a comprehensive rule-based decision engine that
    analyzes customer data to predict churn risk and generate actionable
    retention recommendations. The engine uses business rules and thresholds
    to make decisions that are explainable and auditable.
    """
    
    def __init__(self):
        """Initialize the rule-based decision engine."""
        self.churn_thresholds = ChurnRiskThresholds()
        self.client_segments = ClientSegments()
        self.strategy_categories = StrategyCategories()
        
        # Decision engine configuration
        self.rule_weights = AIModelParams.RULE_WEIGHTS
        self.high_risk_threshold = settings.churn_risk_threshold_high
        self.medium_risk_threshold = settings.churn_risk_threshold_medium
        
        logger.info("Rule-based decision engine initialized")
    
    def analyze_customer_risk(self, customer_data: pd.Series) -> Dict[str, Any]:
        """
        Analyze customer churn risk using rule-based logic.
        
        This method applies a comprehensive set of business rules to analyze
        customer data and determine churn risk levels. The analysis considers
        multiple factors including engagement, revenue, support, and satisfaction.
        
        Args:
            customer_data: Customer profile data with metrics
            
        Returns:
            Dict[str, Any]: Risk analysis results with scores and factors
        """
        logger.debug(f"Analyzing risk for customer {customer_data.get('customer_pk', 'unknown')}")
        
        # Initialize risk factors
        risk_factors = {
            'engagement_risk': 0.0,
            'revenue_risk': 0.0,
            'support_risk': 0.0,
            'satisfaction_risk': 0.0,
            'activity_risk': 0.0
        }
        
        # Calculate engagement risk
        engagement_score = customer_data.get('engagement_score', 0)
        days_since_engagement = customer_data.get('days_since_last_engagement', 999)
        
        if engagement_score < self.churn_thresholds.ENGAGEMENT_LOW:
            risk_factors['engagement_risk'] = 0.8
        elif engagement_score < self.churn_thresholds.ENGAGEMENT_MEDIUM:
            risk_factors['engagement_risk'] = 0.5
        else:
            risk_factors['engagement_risk'] = 0.2
        
        if days_since_engagement > self.churn_thresholds.DAYS_SINCE_ACTIVE_OLD:
            risk_factors['activity_risk'] = 0.9
        elif days_since_engagement > self.churn_thresholds.DAYS_SINCE_ACTIVE_MODERATE:
            risk_factors['activity_risk'] = 0.6
        else:
            risk_factors['activity_risk'] = 0.1
        
        # Calculate revenue risk
        total_revenue = customer_data.get('total_lifetime_revenue', 0)
        avg_transaction_value = customer_data.get('average_transaction_value', 0)
        
        if total_revenue < 1000:  # Low revenue threshold
            risk_factors['revenue_risk'] = 0.7
        elif total_revenue < 5000:  # Medium revenue threshold
            risk_factors['revenue_risk'] = 0.4
        else:
            risk_factors['revenue_risk'] = 0.1
        
        if avg_transaction_value < 100:  # Low transaction value
            risk_factors['revenue_risk'] = min(risk_factors['revenue_risk'] + 0.3, 1.0)
        
        # Calculate support risk
        support_tickets = customer_data.get('total_support_tickets_lifetime', 0)
        satisfaction_score = customer_data.get('avg_satisfaction_score_lifetime', 0)
        
        if support_tickets > 10:  # High support volume
            risk_factors['support_risk'] = 0.8
        elif support_tickets > 5:  # Medium support volume
            risk_factors['support_risk'] = 0.5
        else:
            risk_factors['support_risk'] = 0.2
        
        if satisfaction_score < 3:  # Low satisfaction
            risk_factors['satisfaction_risk'] = 0.9
        elif satisfaction_score < 4:  # Medium satisfaction
            risk_factors['satisfaction_risk'] = 0.6
        else:
            risk_factors['satisfaction_risk'] = 0.1
        
        # Calculate NPS risk
        nps_score = customer_data.get('most_recent_nps_score', 0)
        if nps_score <= self.churn_thresholds.NPS_DETRACTOR:
            risk_factors['satisfaction_risk'] = max(risk_factors['satisfaction_risk'], 0.8)
        elif nps_score <= self.churn_thresholds.NPS_PASSIVE:
            risk_factors['satisfaction_risk'] = max(risk_factors['satisfaction_risk'], 0.5)
        
        # Calculate composite risk score
        composite_risk = (
            risk_factors['engagement_risk'] * self.rule_weights['engagement'] +
            risk_factors['revenue_risk'] * self.rule_weights['revenue'] +
            risk_factors['support_risk'] * self.rule_weights['support'] +
            risk_factors['satisfaction_risk'] * self.rule_weights['nps'] +
            risk_factors['activity_risk'] * 0.1  # Additional weight for activity
        )
        
        # Determine risk level
        if composite_risk >= self.high_risk_threshold:
            risk_level = 'High'
        elif composite_risk >= self.medium_risk_threshold:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        # Identify key risk factors
        key_factors = []
        for factor, score in risk_factors.items():
            if score > 0.6:
                key_factors.append(factor.replace('_risk', '').title())
        
        analysis = {
            'customer_pk': customer_data.get('customer_pk', 'unknown'),
            'composite_risk_score': round(composite_risk, 3),
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'key_factors': key_factors,
            'analysis_date': datetime.now(),
            'confidence': self._calculate_confidence(risk_factors, composite_risk)
        }
        
        logger.debug(f"Risk analysis completed. Risk level: {risk_level}")
        return analysis
    
    def generate_recommendations(self, risk_analysis: Dict[str, Any], 
                                customer_data: pd.Series) -> Dict[str, Any]:
        """
        Generate retention recommendations based on risk analysis.
        
        This method creates specific, actionable recommendations for customer
        retention based on the risk analysis results. Recommendations are
        tailored to the customer's risk profile and business value.
        
        Args:
            risk_analysis: Risk analysis results
            customer_data: Customer profile data
            
        Returns:
            Dict[str, Any]: Retention recommendations and strategies
        """
        logger.debug(f"Generating recommendations for customer {risk_analysis['customer_pk']}")
        
        recommendations = {
            'customer_pk': risk_analysis['customer_pk'],
            'risk_level': risk_analysis['risk_level'],
            'priority': self._calculate_priority(risk_analysis, customer_data),
            'recommended_actions': [],
            'strategies': [],
            'timeline': self._calculate_timeline(risk_analysis),
            'expected_outcome': self._calculate_expected_outcome(risk_analysis),
            'resources_required': self._calculate_resources_required(risk_analysis)
        }
        
        # Generate actions based on risk level
        if risk_analysis['risk_level'] == 'High':
            recommendations['recommended_actions'] = self._get_high_risk_actions(risk_analysis, customer_data)
            recommendations['strategies'] = self._get_high_risk_strategies(risk_analysis, customer_data)
        elif risk_analysis['risk_level'] == 'Medium':
            recommendations['recommended_actions'] = self._get_medium_risk_actions(risk_analysis, customer_data)
            recommendations['strategies'] = self._get_medium_risk_strategies(risk_analysis, customer_data)
        else:
            recommendations['recommended_actions'] = self._get_low_risk_actions(risk_analysis, customer_data)
            recommendations['strategies'] = self._get_low_risk_strategies(risk_analysis, customer_data)
        
        # Add specific recommendations based on key factors
        for factor in risk_analysis['key_factors']:
            if factor == 'Engagement':
                recommendations['recommended_actions'].extend([
                    "Send personalized re-engagement email campaign",
                    "Schedule feature training session",
                    "Provide usage analytics and insights"
                ])
            elif factor == 'Revenue':
                recommendations['recommended_actions'].extend([
                    "Review pricing and value proposition",
                    "Offer retention discount or upgrade",
                    "Conduct business value assessment"
                ])
            elif factor == 'Support':
                recommendations['recommended_actions'].extend([
                    "Assign dedicated support representative",
                    "Conduct support satisfaction survey",
                    "Implement proactive support monitoring"
                ])
            elif factor == 'Satisfaction':
                recommendations['recommended_actions'].extend([
                    "Conduct detailed satisfaction interview",
                    "Address specific pain points",
                    "Implement feedback-driven improvements"
                ])
        
        # Remove duplicates and limit to top 5 actions
        recommendations['recommended_actions'] = list(set(recommendations['recommended_actions']))[:5]
        
        logger.debug(f"Recommendations generated. Actions: {len(recommendations['recommended_actions'])}")
        return recommendations
    
    def _calculate_confidence(self, risk_factors: Dict[str, float], 
                            composite_risk: float) -> str:
        """Calculate confidence level for risk assessment."""
        # High confidence if risk factors are consistent
        factor_variance = np.var(list(risk_factors.values()))
        if factor_variance < 0.1 and composite_risk > 0.7:
            return 'High'
        elif factor_variance < 0.2:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_priority(self, risk_analysis: Dict[str, Any], 
                          customer_data: pd.Series) -> str:
        """Calculate priority level for customer retention."""
        revenue = customer_data.get('total_lifetime_revenue', 0)
        risk_level = risk_analysis['risk_level']
        
        if risk_level == 'High' and revenue > 10000:
            return 'Critical'
        elif risk_level == 'High' and revenue > 5000:
            return 'High'
        elif risk_level == 'Medium' and revenue > 10000:
            return 'High'
        elif risk_level == 'High':
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_timeline(self, risk_analysis: Dict[str, Any]) -> str:
        """Calculate recommended timeline for actions."""
        risk_level = risk_analysis['risk_level']
        
        if risk_level == 'High':
            return 'Immediate (within 24 hours)'
        elif risk_level == 'Medium':
            return 'Urgent (within 1 week)'
        else:
            return 'Standard (within 2 weeks)'
    
    def _calculate_expected_outcome(self, risk_analysis: Dict[str, Any]) -> str:
        """Calculate expected outcome of retention efforts."""
        risk_level = risk_analysis['risk_level']
        confidence = risk_analysis['confidence']
        
        if risk_level == 'High' and confidence == 'High':
            return 'High probability of retention with immediate action'
        elif risk_level == 'High':
            return 'Moderate probability of retention with targeted efforts'
        elif risk_level == 'Medium':
            return 'Good probability of retention with standard approach'
        else:
            return 'Maintain current relationship and monitor'
    
    def _calculate_resources_required(self, risk_analysis: Dict[str, Any]) -> List[str]:
        """Calculate resources required for retention efforts."""
        risk_level = risk_analysis['risk_level']
        key_factors = risk_analysis['key_factors']
        
        resources = []
        
        if risk_level == 'High':
            resources.extend(['Senior Account Manager', 'Dedicated Support Team'])
        
        if 'Engagement' in key_factors:
            resources.append('Customer Success Specialist')
        
        if 'Support' in key_factors:
            resources.append('Technical Support Lead')
        
        if 'Revenue' in key_factors:
            resources.append('Sales Representative')
        
        return list(set(resources))
    
    def _get_high_risk_actions(self, risk_analysis: Dict[str, Any], 
                             customer_data: pd.Series) -> List[str]:
        """Get actions for high-risk customers."""
        actions = [
            "Schedule immediate executive call",
            "Conduct emergency satisfaction survey",
            "Offer retention discount or special terms",
            "Assign dedicated account manager",
            "Implement daily monitoring and alerts"
        ]
        
        # Add revenue-based actions
        revenue = customer_data.get('total_lifetime_revenue', 0)
        if revenue > 10000:
            actions.append("Escalate to C-level executive")
            actions.append("Prepare custom retention proposal")
        
        return actions
    
    def _get_medium_risk_actions(self, risk_analysis: Dict[str, Any], 
                               customer_data: pd.Series) -> List[str]:
        """Get actions for medium-risk customers."""
        actions = [
            "Schedule proactive check-in call",
            "Send personalized engagement content",
            "Offer additional training or support",
            "Conduct quarterly business review",
            "Implement weekly monitoring"
        ]
        
        return actions
    
    def _get_low_risk_actions(self, risk_analysis: Dict[str, Any], 
                            customer_data: pd.Series) -> List[str]:
        """Get actions for low-risk customers."""
        actions = [
            "Maintain regular communication",
            "Share relevant product updates",
            "Identify upsell opportunities",
            "Conduct annual satisfaction survey",
            "Monitor engagement trends"
        ]
        
        return actions
    
    def _get_high_risk_strategies(self, risk_analysis: Dict[str, Any], 
                                customer_data: pd.Series) -> List[str]:
        """Get strategies for high-risk customers."""
        return [
            "Emergency Retention Program",
            "Executive Escalation Protocol",
            "Custom Value Proposition",
            "Dedicated Support Program"
        ]
    
    def _get_medium_risk_strategies(self, risk_analysis: Dict[str, Any], 
                                  customer_data: pd.Series) -> List[str]:
        """Get strategies for medium-risk customers."""
        return [
            "Proactive Engagement Program",
            "Educational Content Campaign",
            "Regular Check-in Protocol",
            "Feature Adoption Program"
        ]
    
    def _get_low_risk_strategies(self, risk_analysis: Dict[str, Any], 
                               customer_data: pd.Series) -> List[str]:
        """Get strategies for low-risk customers."""
        return [
            "Relationship Building Program",
            "Upsell Opportunity Identification",
            "Referral Program",
            "Loyalty Rewards Program"
        ]
    
    def process_customer_batch(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Process a batch of customers for risk analysis and recommendations.
        
        This method processes multiple customers at once, applying the rule-based
        decision engine to each customer and generating comprehensive results
        for batch processing and analysis.
        
        Args:
            customers_df: DataFrame of customer profiles
            
        Returns:
            pd.DataFrame: Results with risk analysis and recommendations
        """
        logger.info(f"Processing customer batch: {len(customers_df)} customers")
        
        results = []
        
        for _, customer in customers_df.iterrows():
            try:
                # Analyze risk
                risk_analysis = self.analyze_customer_risk(customer)
                
                # Generate recommendations
                recommendations = self.generate_recommendations(risk_analysis, customer)
                
                # Combine results
                result = {
                    'customer_pk': customer.get('customer_pk', 'unknown'),
                    'risk_score': risk_analysis['composite_risk_score'],
                    'risk_level': risk_analysis['risk_level'],
                    'priority': recommendations['priority'],
                    'recommended_action': recommendations['recommended_actions'][0] if recommendations['recommended_actions'] else 'Monitor',
                    'timeline': recommendations['timeline'],
                    'expected_outcome': recommendations['expected_outcome'],
                    'key_factors': ', '.join(risk_analysis['key_factors']),
                    'confidence': risk_analysis['confidence']
                }
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error processing customer {customer.get('customer_pk', 'unknown')}: {str(e)}")
                # Add error result
                results.append({
                    'customer_pk': customer.get('customer_pk', 'unknown'),
                    'risk_score': 0.0,
                    'risk_level': 'Unknown',
                    'priority': 'Unknown',
                    'recommended_action': 'Error in analysis',
                    'timeline': 'Unknown',
                    'expected_outcome': 'Analysis failed',
                    'key_factors': 'Error',
                    'confidence': 'Low'
                })
        
        results_df = pd.DataFrame(results)
        
        logger.info(f"Customer batch processing completed. Results: {len(results_df)}")
        return results_df
    
    def get_decision_summary(self, results_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary statistics for decision engine results.
        
        This method creates comprehensive summary statistics for the decision
        engine results, including risk distribution, priority levels, and
        recommended actions for monitoring and reporting.
        
        Args:
            results_df: Decision engine results DataFrame
            
        Returns:
            Dict[str, Any]: Summary statistics and insights
        """
        logger.info("Generating decision engine summary")
        
        summary = {
            'total_customers': len(results_df),
            'risk_distribution': results_df['risk_level'].value_counts().to_dict(),
            'priority_distribution': results_df['priority'].value_counts().to_dict(),
            'average_risk_score': results_df['risk_score'].mean(),
            'high_risk_customers': len(results_df[results_df['risk_level'] == 'High']),
            'critical_priority_customers': len(results_df[results_df['priority'] == 'Critical']),
            'top_recommended_actions': results_df['recommended_action'].value_counts().head(10).to_dict(),
            'confidence_distribution': results_df['confidence'].value_counts().to_dict()
        }
        
        # Calculate insights
        insights = []
        
        if summary['high_risk_customers'] > 0:
            insights.append(f"{summary['high_risk_customers']} customers require immediate attention")
        
        if summary['critical_priority_customers'] > 0:
            insights.append(f"{summary['critical_priority_customers']} customers are critical priority")
        
        if summary['average_risk_score'] > 0.6:
            insights.append("Overall risk level is elevated - consider proactive measures")
        
        summary['insights'] = insights
        summary['generated_at'] = datetime.now()
        
        logger.info("Decision engine summary generated")
        return summary

def main():
    """Main function to demonstrate rule-based decision engine functionality."""
    logger.info("Starting A.U.R.A rule-based decision engine demonstration")
    
    # Initialize decision engine
    decision_engine = RuleBasedDecisionEngine()
    
    # Create sample customer data
    sample_customers = pd.DataFrame({
        'customer_pk': ['CUST_001', 'CUST_002', 'CUST_003'],
        'engagement_score': [0.2, 0.6, 0.8],
        'days_since_last_engagement': [45, 15, 5],
        'total_lifetime_revenue': [500, 5000, 15000],
        'average_transaction_value': [50, 200, 500],
        'total_support_tickets_lifetime': [8, 3, 1],
        'avg_satisfaction_score_lifetime': [2.5, 4.0, 4.8],
        'most_recent_nps_score': [3, 7, 9]
    })
    
    # Process customer batch
    results = decision_engine.process_customer_batch(sample_customers)
    
    # Generate summary
    summary = decision_engine.get_decision_summary(results)
    
    # Print results
    print("\n" + "="*50)
    print("A.U.R.A Decision Engine Results")
    print("="*50)
    print(f"Total customers: {summary['total_customers']}")
    print(f"Risk distribution: {summary['risk_distribution']}")
    print(f"Average risk score: {summary['average_risk_score']:.3f}")
    print(f"High risk customers: {summary['high_risk_customers']}")
    print(f"Critical priority: {summary['critical_priority_customers']}")
    
    print("\nCustomer Results:")
    for _, row in results.iterrows():
        print(f"  {row['customer_pk']}: {row['risk_level']} risk, {row['priority']} priority")
        print(f"    Action: {row['recommended_action']}")
    
    logger.info("A.U.R.A decision engine demonstration completed")

if __name__ == "__main__":
    main()

