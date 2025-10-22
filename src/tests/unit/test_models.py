# A.U.R.A (AI-Unified Retention Analytics) - Models Unit Tests
# This module contains unit tests for the AI models and decision engine
# to ensure accurate predictions and recommendations

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.models.forecasting.prophet_model import ProphetForecasting
from src.models.decision_engine.rules_engine import RulesEngine
from src.config.settings import settings

class TestProphetForecasting(unittest.TestCase):
    """Test cases for Prophet forecasting model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.forecasting = ProphetForecasting()
        
        # Create sample time series data
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        values = np.random.normal(100, 10, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365)
        
        self.sample_data = pd.DataFrame({
            'ds': dates,
            'y': values
        })
    
    def test_prepare_data(self):
        """Test data preparation for Prophet model."""
        prepared_data = self.forecasting.prepare_data(self.sample_data)
        
        self.assertIsInstance(prepared_data, pd.DataFrame)
        self.assertIn('ds', prepared_data.columns)
        self.assertIn('y', prepared_data.columns)
        self.assertEqual(len(prepared_data), len(self.sample_data))
    
    def test_train_model(self):
        """Test training Prophet model."""
        # Test with sample data
        model = self.forecasting.train_model(self.sample_data)
        
        self.assertIsNotNone(model)
        self.assertTrue(hasattr(model, 'predict'))
        self.assertTrue(hasattr(model, 'fit'))
    
    def test_make_predictions(self):
        """Test making predictions with trained model."""
        # Train model first
        model = self.forecasting.train_model(self.sample_data)
        
        # Make predictions
        predictions = self.forecasting.make_predictions(model, periods=30)
        
        self.assertIsInstance(predictions, pd.DataFrame)
        self.assertIn('ds', predictions.columns)
        self.assertIn('yhat', predictions.columns)
        self.assertEqual(len(predictions), 30)
    
    def test_evaluate_model(self):
        """Test model evaluation."""
        # Split data for training and testing
        train_data = self.sample_data.iloc[:-30]
        test_data = self.sample_data.iloc[-30:]
        
        # Train model
        model = self.forecasting.train_model(train_data)
        
        # Evaluate model
        metrics = self.forecasting.evaluate_model(model, test_data)
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('mae', metrics)
        self.assertIn('rmse', metrics)
        self.assertIn('mape', metrics)
        
        # Check that metrics are reasonable
        self.assertGreaterEqual(metrics['mae'], 0)
        self.assertGreaterEqual(metrics['rmse'], 0)
        self.assertGreaterEqual(metrics['mape'], 0)
    
    def test_forecast_revenue(self):
        """Test revenue forecasting functionality."""
        # Create sample revenue data
        revenue_data = pd.DataFrame({
            'ds': pd.date_range(start='2023-01-01', end='2023-12-31', freq='M'),
            'y': np.random.normal(10000, 1000, 12)
        })
        
        # Test revenue forecasting
        forecast = self.forecasting.forecast_revenue(revenue_data, periods=6)
        
        self.assertIsInstance(forecast, pd.DataFrame)
        self.assertIn('ds', forecast.columns)
        self.assertIn('yhat', forecast.columns)
        self.assertEqual(len(forecast), 6)
    
    def test_forecast_engagement(self):
        """Test engagement forecasting functionality."""
        # Create sample engagement data
        engagement_data = pd.DataFrame({
            'ds': pd.date_range(start='2023-01-01', end='2023-12-31', freq='D'),
            'y': np.random.uniform(0, 1, 365)
        })
        
        # Test engagement forecasting
        forecast = self.forecasting.forecast_engagement(engagement_data, periods=30)
        
        self.assertIsInstance(forecast, pd.DataFrame)
        self.assertIn('ds', forecast.columns)
        self.assertIn('yhat', forecast.columns)
        self.assertEqual(len(forecast), 30)

class TestRulesEngine(unittest.TestCase):
    """Test cases for rules-based decision engine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.rules_engine = RulesEngine()
        
        # Create sample customer data
        self.sample_customers = pd.DataFrame({
            'customer_pk': ['CUST_001', 'CUST_002', 'CUST_003', 'CUST_004'],
            'engagement_score': [0.8, 0.3, 0.6, 0.9],
            'total_lifetime_revenue': [5000.0, 1000.0, 3000.0, 8000.0],
            'support_ticket_count': [1, 8, 3, 0],
            'nps_score': [9, 3, 7, 10],
            'days_since_last_login': [5, 45, 15, 2],
            'subscription_plan': ['Premium', 'Basic', 'Standard', 'Enterprise']
        })
    
    def test_classify_churn_risk(self):
        """Test churn risk classification."""
        for _, customer in self.sample_customers.iterrows():
            risk_level = self.rules_engine.classify_churn_risk(customer)
            
            self.assertIn(risk_level, ['Low', 'Medium', 'High'])
            
            # Test specific cases
            if customer['engagement_score'] < 0.3 or customer['days_since_last_login'] > 30:
                self.assertEqual(risk_level, 'High')
            elif customer['engagement_score'] < 0.6 or customer['support_ticket_count'] > 5:
                self.assertEqual(risk_level, 'Medium')
            else:
                self.assertEqual(risk_level, 'Low')
    
    def test_generate_recommendations(self):
        """Test generating customer recommendations."""
        for _, customer in self.sample_customers.iterrows():
            recommendations = self.rules_engine.generate_recommendations(customer)
            
            self.assertIsInstance(recommendations, list)
            self.assertGreater(len(recommendations), 0)
            
            # Test that recommendations are relevant
            for rec in recommendations:
                self.assertIsInstance(rec, str)
                self.assertGreater(len(rec), 0)
    
    def test_identify_upsell_opportunities(self):
        """Test identifying upsell opportunities."""
        upsell_opportunities = self.rules_engine.identify_upsell_opportunities(self.sample_customers)
        
        self.assertIsInstance(upsell_opportunities, pd.DataFrame)
        self.assertIn('customer_pk', upsell_opportunities.columns)
        self.assertIn('upsell_potential', upsell_opportunities.columns)
        self.assertIn('recommended_action', upsell_opportunities.columns)
    
    def test_calculate_retention_score(self):
        """Test calculating retention scores."""
        for _, customer in self.sample_customers.iterrows():
            retention_score = self.rules_engine.calculate_retention_score(customer)
            
            self.assertIsInstance(retention_score, (int, float))
            self.assertGreaterEqual(retention_score, 0)
            self.assertLessEqual(retention_score, 100)
    
    def test_apply_business_rules(self):
        """Test applying business rules to customer data."""
        result = self.rules_engine.apply_business_rules(self.sample_customers)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('churn_risk_level', result.columns)
        self.assertIn('retention_score', result.columns)
        self.assertIn('recommended_actions', result.columns)
        
        # Test that all customers have been processed
        self.assertEqual(len(result), len(self.sample_customers))
    
    def test_rule_consistency(self):
        """Test that rules are applied consistently."""
        # Test the same customer multiple times
        customer = self.sample_customers.iloc[0]
        
        risk1 = self.rules_engine.classify_churn_risk(customer)
        risk2 = self.rules_engine.classify_churn_risk(customer)
        
        self.assertEqual(risk1, risk2)
        
        rec1 = self.rules_engine.generate_recommendations(customer)
        rec2 = self.rules_engine.generate_recommendations(customer)
        
        self.assertEqual(rec1, rec2)
    
    def test_edge_cases(self):
        """Test edge cases in rules engine."""
        # Test with extreme values
        extreme_customer = pd.Series({
            'engagement_score': 0.0,
            'total_lifetime_revenue': 0.0,
            'support_ticket_count': 100,
            'nps_score': 0,
            'days_since_last_login': 365
        })
        
        risk_level = self.rules_engine.classify_churn_risk(extreme_customer)
        self.assertEqual(risk_level, 'High')
        
        recommendations = self.rules_engine.generate_recommendations(extreme_customer)
        self.assertGreater(len(recommendations), 0)
        
        # Test with perfect values
        perfect_customer = pd.Series({
            'engagement_score': 1.0,
            'total_lifetime_revenue': 100000.0,
            'support_ticket_count': 0,
            'nps_score': 10,
            'days_since_last_login': 0
        })
        
        risk_level = self.rules_engine.classify_churn_risk(perfect_customer)
        self.assertEqual(risk_level, 'Low')
        
        recommendations = self.rules_engine.generate_recommendations(perfect_customer)
        self.assertGreater(len(recommendations), 0)

class TestModelIntegration(unittest.TestCase):
    """Test cases for model integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.forecasting = ProphetForecasting()
        self.rules_engine = RulesEngine()
    
    def test_forecasting_and_rules_integration(self):
        """Test integration between forecasting and rules engine."""
        # Create sample data
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        values = np.random.normal(100, 10, len(dates))
        
        time_series_data = pd.DataFrame({
            'ds': dates,
            'y': values
        })
        
        # Train forecasting model
        model = self.forecasting.train_model(time_series_data)
        predictions = self.forecasting.make_predictions(model, periods=30)
        
        # Test that predictions can be used with rules engine
        self.assertIsInstance(predictions, pd.DataFrame)
        self.assertIn('yhat', predictions.columns)
        
        # Test that rules engine can process forecasted data
        forecast_customer = pd.Series({
            'engagement_score': 0.7,
            'total_lifetime_revenue': 5000.0,
            'support_ticket_count': 2,
            'nps_score': 8,
            'days_since_last_login': 10
        })
        
        risk_level = self.rules_engine.classify_churn_risk(forecast_customer)
        self.assertIn(risk_level, ['Low', 'Medium', 'High'])
    
    def test_model_performance(self):
        """Test model performance metrics."""
        # Create sample data for performance testing
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        values = np.random.normal(100, 10, len(dates))
        
        time_series_data = pd.DataFrame({
            'ds': dates,
            'y': values
        })
        
        # Split data for training and testing
        train_data = time_series_data.iloc[:-30]
        test_data = time_series_data.iloc[-30:]
        
        # Train model and evaluate
        model = self.forecasting.train_model(train_data)
        metrics = self.forecasting.evaluate_model(model, test_data)
        
        # Test that metrics are reasonable
        self.assertLess(metrics['mae'], 100)  # Mean Absolute Error should be reasonable
        self.assertLess(metrics['rmse'], 100)  # Root Mean Square Error should be reasonable
        self.assertLess(metrics['mape'], 50)  # Mean Absolute Percentage Error should be reasonable

def run_tests():
    """Run all model tests."""
    print("Running A.U.R.A Models Tests...")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestProphetForecasting))
    test_suite.addTest(unittest.makeSuite(TestRulesEngine))
    test_suite.addTest(unittest.makeSuite(TestModelIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print results
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        exit(1)
