# A.U.R.A AI Model Integration for Chatbot
# This module provides AI-powered churn prediction capabilities for the chatbot

import pickle
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AURAAIModel:
    """
    A.U.R.A AI Model wrapper for churn prediction and customer insights.
    
    This class integrates the trained XGBoost model for intelligent customer
    retention analysis and provides AI-powered responses for the chatbot.
    """
    
    def __init__(self, model_path: str = "Ai_Model/aura_churn_model.pkl"):
        """
        Initialize the AURA AI model.
        
        Args:
            model_path: Path to the trained XGBoost model file
        """
        self.model_path = model_path
        self.model = None
        self.preprocessor = None
        self.feature_names = None
        self.is_loaded = False
        
        # Expected feature names based on typical customer data
        self.expected_features = [
            'customer_id', 'age', 'gender', 'subscription_plan', 'monthly_revenue',
            'total_revenue', 'engagement_score', 'health_score', 'days_since_last_login',
            'support_tickets_count', 'nps_score', 'satisfaction_score', 'feature_usage_count',
            'session_duration_avg', 'page_views_count', 'bounce_rate', 'conversion_rate',
            'retention_rate', 'churn_risk_score', 'lifetime_value', 'acquisition_cost',
            'revenue_growth_rate', 'engagement_trend', 'support_satisfaction',
            'product_adoption_rate', 'feature_adoption_rate', 'usage_frequency',
            'session_frequency', 'content_engagement', 'social_engagement',
            'email_engagement', 'push_notification_engagement', 'mobile_usage',
            'desktop_usage', 'tablet_usage', 'premium_features_usage',
            'community_participation', 'referral_count', 'referral_success_rate',
            'upgrade_count', 'downgrade_count', 'cancellation_attempts',
            'payment_failures', 'subscription_length', 'trial_to_paid_conversion',
            'seasonal_usage_pattern', 'geographic_region', 'device_type_preference'
        ]
        
        self._load_model()
    
    def _load_model(self) -> bool:
        """
        Load the trained XGBoost model and preprocessor.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.model_path):
                logger.warning(f"Model file not found: {self.model_path}")
                return False
            
            # Load the XGBoost model
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            logger.info(f"Successfully loaded XGBoost model: {type(self.model)}")
            logger.info(f"Model has {self.model.n_features_in_} input features")
            logger.info(f"Model classes: {self.model.classes_}")
            
            # Set feature names based on model expectations
            self.feature_names = [f"feature_{i}" for i in range(self.model.n_features_in_)]
            
            self.is_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to load AI model: {e}")
            self.is_loaded = False
            return False
    
    def predict_churn_risk(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict churn risk for a customer using the AI model.
        
        Args:
            customer_data: Dictionary containing customer information
            
        Returns:
            Dict containing prediction results and insights
        """
        if not self.is_loaded:
            return {
                'error': 'AI model not loaded',
                'churn_probability': 0.0,
                'risk_level': 'Unknown',
                'confidence': 0.0
            }
        
        try:
            # Prepare feature vector for the model
            feature_vector = self._prepare_features(customer_data)
            
            if feature_vector is None:
                return {
                    'error': 'Could not prepare features for prediction',
                    'churn_probability': 0.0,
                    'risk_level': 'Unknown',
                    'confidence': 0.0
                }
            
            # Make prediction
            churn_probability = self.model.predict_proba(feature_vector)[0][1]  # Probability of churn (class 1)
            churn_prediction = self.model.predict(feature_vector)[0]
            
            # Determine risk level based on probability
            if churn_probability >= 0.7:
                risk_level = 'High'
            elif churn_probability >= 0.4:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
            
            # Calculate confidence based on probability distance from 0.5
            confidence = abs(churn_probability - 0.5) * 2
            
            # Get feature importance for this prediction
            feature_importance = self._get_feature_importance(feature_vector)
            
            return {
                'churn_probability': float(churn_probability),
                'churn_prediction': int(churn_prediction),
                'risk_level': risk_level,
                'confidence': float(confidence),
                'feature_importance': feature_importance,
                'model_used': 'XGBoost',
                'prediction_quality': 'High' if confidence > 0.6 else 'Medium' if confidence > 0.3 else 'Low'
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {
                'error': f'Prediction failed: {str(e)}',
                'churn_probability': 0.0,
                'risk_level': 'Unknown',
                'confidence': 0.0
            }
    
    def _prepare_features(self, customer_data: Dict[str, Any]) -> Optional[np.ndarray]:
        """
        Prepare feature vector for the AI model.
        
        Args:
            customer_data: Raw customer data dictionary
            
        Returns:
            numpy array of features ready for model prediction
        """
        try:
            # Create a feature vector with the expected number of features
            features = np.zeros(self.model.n_features_in_)
            
            # Map customer data to features (simplified mapping)
            feature_mapping = {
                'age': 0, 'monthly_revenue': 1, 'total_revenue': 2, 'engagement_score': 3,
                'health_score': 4, 'days_since_last_login': 5, 'support_tickets_count': 6,
                'nps_score': 7, 'satisfaction_score': 8, 'feature_usage_count': 9,
                'session_duration_avg': 10, 'page_views_count': 11, 'bounce_rate': 12,
                'conversion_rate': 13, 'retention_rate': 14, 'lifetime_value': 15,
                'acquisition_cost': 16, 'revenue_growth_rate': 17, 'engagement_trend': 18,
                'support_satisfaction': 19, 'product_adoption_rate': 20, 'feature_adoption_rate': 21,
                'usage_frequency': 22, 'session_frequency': 23, 'content_engagement': 24,
                'social_engagement': 25, 'email_engagement': 26, 'push_notification_engagement': 27,
                'mobile_usage': 28, 'desktop_usage': 29, 'tablet_usage': 30,
                'premium_features_usage': 31, 'community_participation': 32, 'referral_count': 33,
                'referral_success_rate': 34, 'upgrade_count': 35, 'downgrade_count': 36,
                'cancellation_attempts': 37, 'payment_failures': 38, 'subscription_length': 39,
                'trial_to_paid_conversion': 40, 'seasonal_usage_pattern': 41, 'geographic_region': 42,
                'device_type_preference': 43, 'subscription_plan_encoded': 44
            }
            
            # Fill in available features
            for key, value in customer_data.items():
                if key in feature_mapping:
                    idx = feature_mapping[key]
                    if idx < len(features):
                        # Convert to numeric if possible
                        try:
                            features[idx] = float(value) if value is not None else 0.0
                        except (ValueError, TypeError):
                            features[idx] = 0.0
                elif key == 'subscription_plan':
                    # Encode subscription plan
                    plan_encoding = {'Basic': 1, 'Standard': 2, 'Premium': 3, 'Enterprise': 4}
                    features[44] = plan_encoding.get(value, 1)
            
            # Fill remaining features with default values
            for i in range(len(features)):
                if features[i] == 0.0:
                    features[i] = np.random.normal(0, 0.1)  # Small random noise for missing features
            
            return features.reshape(1, -1)
            
        except Exception as e:
            logger.error(f"Feature preparation failed: {e}")
            return None
    
    def _get_feature_importance(self, feature_vector: np.ndarray) -> Dict[str, float]:
        """
        Get feature importance for the prediction.
        
        Args:
            feature_vector: Input features for the model
            
        Returns:
            Dictionary of feature importance scores
        """
        try:
            if hasattr(self.model, 'feature_importances_'):
                importance_scores = self.model.feature_importances_
                # Get top 10 most important features
                top_indices = np.argsort(importance_scores)[-10:]
                
                feature_importance = {}
                for idx in top_indices:
                    feature_name = f"feature_{idx}"
                    feature_importance[feature_name] = float(importance_scores[idx])
                
                return feature_importance
            else:
                return {}
                
        except Exception as e:
            logger.error(f"Feature importance calculation failed: {e}")
            return {}
    
    def get_ai_insights(self, customer_data: Dict[str, Any]) -> str:
        """
        Generate AI-powered insights for customer retention.
        
        Args:
            customer_data: Customer information dictionary
            
        Returns:
            String containing AI-generated insights and recommendations
        """
        if not self.is_loaded:
            return "AI model not available. Please ensure the model is properly loaded."
        
        # Get churn prediction
        prediction_result = self.predict_churn_risk(customer_data)
        
        if 'error' in prediction_result:
            return f"AI Analysis Error: {prediction_result['error']}"
        
        churn_prob = prediction_result['churn_probability']
        risk_level = prediction_result['risk_level']
        confidence = prediction_result['confidence']
        
        # Generate insights based on prediction
        insights = []
        
        if risk_level == 'High':
            insights.append("🚨 **HIGH CHURN RISK DETECTED**")
            insights.append(f"• Churn probability: {churn_prob:.1%}")
            insights.append("• **Immediate action required**")
            insights.append("• Recommend: Personal retention call within 24 hours")
            insights.append("• Offer: Exclusive discount or premium feature access")
            insights.append("• Assign: Dedicated customer success manager")
            
        elif risk_level == 'Medium':
            insights.append("⚠️ **MEDIUM CHURN RISK**")
            insights.append(f"• Churn probability: {churn_prob:.1%}")
            insights.append("• **Proactive engagement needed**")
            insights.append("• Recommend: Enhanced onboarding and training")
            insights.append("• Offer: Feature tutorials and best practices")
            insights.append("• Monitor: Weekly check-ins for next month")
            
        else:
            insights.append("✅ **LOW CHURN RISK**")
            insights.append(f"• Churn probability: {churn_prob:.1%}")
            insights.append("• **Customer is healthy and engaged**")
            insights.append("• Recommend: Upselling opportunities")
            insights.append("• Offer: Premium features or plan upgrades")
            insights.append("• Focus: Referral program participation")
        
        # Add confidence and model information
        insights.append(f"\n**AI Model Confidence:** {confidence:.1%}")
        insights.append(f"**Prediction Quality:** {prediction_result.get('prediction_quality', 'Unknown')}")
        insights.append(f"**Model Used:** {prediction_result.get('model_used', 'Unknown')}")
        
        # Add feature importance insights
        if prediction_result.get('feature_importance'):
            insights.append("\n**Key Risk Factors:**")
            for feature, importance in list(prediction_result['feature_importance'].items())[:5]:
                insights.append(f"• {feature}: {importance:.3f}")
        
        return "\n".join(insights)
    
    def get_model_status(self) -> Dict[str, Any]:
        """
        Get the current status of the AI model.
        
        Returns:
            Dictionary containing model status information
        """
        return {
            'is_loaded': self.is_loaded,
            'model_type': str(type(self.model)) if self.model else 'None',
            'feature_count': self.model.n_features_in_ if self.model else 0,
            'model_classes': self.model.classes_.tolist() if self.model else [],
            'model_path': self.model_path
        }

# Global instance for the chatbot
aura_ai_model = AURAAIModel()

