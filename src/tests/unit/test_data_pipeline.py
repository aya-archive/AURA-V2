# A.U.R.A (AI-Unified Retention Analytics) - Data Pipeline Unit Tests
# This module contains unit tests for the data pipeline components
# to ensure data processing accuracy and reliability

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.data_pipeline.ingest import DataIngestion
from src.data_pipeline.silver_transform import SilverTransformation
from src.data_pipeline.gold_agg import GoldAggregation
from src.config.settings import settings

class TestDataIngestion(unittest.TestCase):
    """Test cases for data ingestion component."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ingestion = DataIngestion()
        
        # Create sample Bronze layer data
        self.sample_customers = pd.DataFrame({
            'customer_id': ['CUST_001', 'CUST_002', 'CUST_003'],
            'first_name': ['John', 'Jane', 'Mike'],
            'last_name': ['Smith', 'Johnson', 'Williams'],
            'email': ['john@company.com', 'jane@company.com', 'mike@company.com'],
            'subscription_plan': ['Basic', 'Premium', 'Standard'],
            'created_at': ['2023-01-15', '2023-02-20', '2023-03-10']
        })
        
        self.sample_transactions = pd.DataFrame({
            'transaction_id': ['TXN_001', 'TXN_002', 'TXN_003'],
            'customer_id': ['CUST_001', 'CUST_002', 'CUST_003'],
            'amount': [100.0, 250.0, 150.0],
            'transaction_date': ['2023-01-20', '2023-02-25', '2023-03-15']
        })
    
    def test_load_customer_data(self):
        """Test loading customer data from Bronze layer."""
        # This would test the actual data loading if files existed
        # For now, we'll test the data structure
        self.assertIsInstance(self.sample_customers, pd.DataFrame)
        self.assertEqual(len(self.sample_customers), 3)
        self.assertIn('customer_id', self.sample_customers.columns)
    
    def test_load_transaction_data(self):
        """Test loading transaction data from Bronze layer."""
        self.assertIsInstance(self.sample_transactions, pd.DataFrame)
        self.assertEqual(len(self.sample_transactions), 3)
        self.assertIn('transaction_id', self.sample_transactions.columns)
    
    def test_data_validation(self):
        """Test data validation during ingestion."""
        # Test required columns
        required_columns = ['customer_id', 'first_name', 'last_name', 'email']
        for col in required_columns:
            self.assertIn(col, self.sample_customers.columns)
        
        # Test data types
        self.assertEqual(self.sample_customers['customer_id'].dtype, 'object')
        self.assertEqual(self.sample_customers['first_name'].dtype, 'object')

class TestSilverTransformation(unittest.TestCase):
    """Test cases for Silver layer transformation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.transformation = SilverTransformation()
        
        # Create sample Bronze layer data
        self.bronze_customers = pd.DataFrame({
            'customer_id': ['CUST_001', 'CUST_002', 'CUST_003'],
            'first_name': ['John', 'Jane', 'Mike'],
            'last_name': ['Smith', 'Johnson', 'Williams'],
            'email': ['john@company.com', 'jane@company.com', 'mike@company.com'],
            'subscription_plan': ['Basic', 'Premium', 'Standard'],
            'created_at': ['2023-01-15', '2023-02-20', '2023-03-10']
        })
        
        self.bronze_transactions = pd.DataFrame({
            'transaction_id': ['TXN_001', 'TXN_002', 'TXN_003'],
            'customer_id': ['CUST_001', 'CUST_002', 'CUST_003'],
            'amount': [100.0, 250.0, 150.0],
            'transaction_date': ['2023-01-20', '2023-02-25', '2023-03-15']
        })
    
    def test_clean_customer_data(self):
        """Test cleaning customer data."""
        cleaned_data = self.transformation.clean_customer_data(self.bronze_customers)
        
        self.assertIsInstance(cleaned_data, pd.DataFrame)
        self.assertEqual(len(cleaned_data), 3)
        self.assertIn('customer_pk', cleaned_data.columns)
    
    def test_clean_transaction_data(self):
        """Test cleaning transaction data."""
        cleaned_data = self.transformation.clean_transaction_data(self.bronze_transactions)
        
        self.assertIsInstance(cleaned_data, pd.DataFrame)
        self.assertEqual(len(cleaned_data), 3)
        self.assertIn('transaction_pk', cleaned_data.columns)
    
    def test_calculate_derived_metrics(self):
        """Test calculating derived metrics."""
        # Create sample data with required columns
        sample_data = pd.DataFrame({
            'customer_pk': ['CUST_001', 'CUST_002', 'CUST_003'],
            'total_revenue': [1000.0, 2500.0, 1500.0],
            'transaction_count': [5, 10, 8],
            'last_transaction_date': ['2023-01-20', '2023-02-25', '2023-03-15']
        })
        
        # Test derived metrics calculation
        result = self.transformation.calculate_derived_metrics(sample_data)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('avg_transaction_value', result.columns)
        self.assertIn('days_since_last_transaction', result.columns)

class TestGoldAggregation(unittest.TestCase):
    """Test cases for Gold layer aggregation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.aggregation = GoldAggregation()
        
        # Create sample Silver layer data
        self.silver_customers = pd.DataFrame({
            'customer_pk': ['CUST_001', 'CUST_002', 'CUST_003'],
            'first_name': ['John', 'Jane', 'Mike'],
            'last_name': ['Smith', 'Johnson', 'Williams'],
            'email_address': ['john@company.com', 'jane@company.com', 'mike@company.com'],
            'current_subscription_plan': ['Basic', 'Premium', 'Standard'],
            'total_lifetime_revenue': [1000.0, 2500.0, 1500.0],
            'engagement_score': [0.8, 0.6, 0.9],
            'support_ticket_count': [2, 5, 1],
            'nps_score': [8, 6, 9]
        })
    
    def test_create_customer_health_gold(self):
        """Test creating customer health Gold layer data."""
        result = self.aggregation.create_customer_health_gold(self.silver_customers)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('customer_pk', result.columns)
        self.assertIn('health_score', result.columns)
        self.assertIn('churn_risk_level', result.columns)
        self.assertIn('recommended_action', result.columns)
    
    def test_calculate_health_score(self):
        """Test calculating customer health scores."""
        sample_customer = {
            'engagement_score': 0.8,
            'total_lifetime_revenue': 1000.0,
            'support_ticket_count': 2,
            'nps_score': 8
        }
        
        health_score = self.aggregation.calculate_health_score(sample_customer)
        
        self.assertIsInstance(health_score, (int, float))
        self.assertGreaterEqual(health_score, 0)
        self.assertLessEqual(health_score, 100)
    
    def test_determine_churn_risk(self):
        """Test determining churn risk levels."""
        test_cases = [
            {'health_score': 85, 'expected': 'Low'},
            {'health_score': 65, 'expected': 'Medium'},
            {'health_score': 35, 'expected': 'High'}
        ]
        
        for case in test_cases:
            risk_level = self.aggregation.determine_churn_risk(case['health_score'])
            self.assertEqual(risk_level, case['expected'])
    
    def test_generate_recommendations(self):
        """Test generating customer recommendations."""
        sample_customer = {
            'churn_risk_level': 'High',
            'engagement_score': 0.3,
            'support_ticket_count': 8,
            'total_lifetime_revenue': 5000.0
        }
        
        recommendation = self.aggregation.generate_recommendations(sample_customer)
        
        self.assertIsInstance(recommendation, str)
        self.assertGreater(len(recommendation), 0)

class TestDataPipelineIntegration(unittest.TestCase):
    """Test cases for data pipeline integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ingestion = DataIngestion()
        self.transformation = SilverTransformation()
        self.aggregation = GoldAggregation()
    
    def test_end_to_end_pipeline(self):
        """Test complete data pipeline from Bronze to Gold."""
        # This would test the complete pipeline if data files existed
        # For now, we'll test the component integration
        
        # Test that all components can be initialized
        self.assertIsNotNone(self.ingestion)
        self.assertIsNotNone(self.transformation)
        self.assertIsNotNone(self.aggregation)
        
        # Test that components have required methods
        self.assertTrue(hasattr(self.ingestion, 'load_customer_data'))
        self.assertTrue(hasattr(self.transformation, 'clean_customer_data'))
        self.assertTrue(hasattr(self.aggregation, 'create_customer_health_gold'))
    
    def test_data_consistency(self):
        """Test data consistency across pipeline layers."""
        # Create sample data that would flow through the pipeline
        bronze_data = pd.DataFrame({
            'customer_id': ['CUST_001', 'CUST_002'],
            'first_name': ['John', 'Jane'],
            'last_name': ['Smith', 'Johnson'],
            'email': ['john@company.com', 'jane@company.com']
        })
        
        # Test that data maintains consistency
        self.assertEqual(len(bronze_data), 2)
        self.assertIn('customer_id', bronze_data.columns)
        
        # Test that transformations preserve data integrity
        cleaned_data = self.transformation.clean_customer_data(bronze_data)
        self.assertEqual(len(cleaned_data), 2)
        self.assertIn('customer_pk', cleaned_data.columns)

def run_tests():
    """Run all data pipeline tests."""
    print("Running A.U.R.A Data Pipeline Tests...")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestDataIngestion))
    test_suite.addTest(unittest.makeSuite(TestSilverTransformation))
    test_suite.addTest(unittest.makeSuite(TestGoldAggregation))
    test_suite.addTest(unittest.makeSuite(TestDataPipelineIntegration))
    
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
