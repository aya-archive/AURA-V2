#!/usr/bin/env python3
"""
A.U.R.A Mock Data Generator
===========================

This script generates realistic mock data for the A.U.R.A platform's Bronze layer.
The data includes correlated signals for churn prediction and represents a realistic
client base with various engagement patterns, revenue levels, and risk profiles.

The generated data follows the Medallion architecture Bronze layer schema and
includes all required entities for the A.U.R.A platform.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os
from pathlib import Path

# Set random seed for reproducible data
np.random.seed(42)
random.seed(42)

class MockDataGenerator:
    """
    Generates realistic mock data for A.U.R.A platform.
    
    This class creates correlated datasets that simulate real client behavior
    patterns, including churn signals, engagement trends, and business metrics.
    The data is designed to test the complete A.U.R.A pipeline from Bronze
    through Gold layers.
    """
    
    def __init__(self):
        """Initialize the mock data generator with base parameters."""
        self.start_date = datetime.now() - timedelta(days=365)  # 1 year of data
        self.end_date = datetime.now()
        self.customer_count = 500
        self.transaction_count = 2000
        self.engagement_events = 5000
        self.support_tickets = 300
        self.survey_responses = 200
        
        # Create data directory if it doesn't exist
        self.data_dir = Path("data/bronze")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_customer_demographics(self) -> pd.DataFrame:
        """
        Generate customer demographics data.
        
        Creates realistic customer profiles with demographics, subscription types,
        and account information. Includes correlation between customer attributes
        and churn risk factors.
        
        Returns:
            pd.DataFrame: Customer demographics with churn risk indicators
        """
        print("Generating customer demographics...")
        
        # Base customer data
        customer_ids = [f"CUST_{i:04d}" for i in range(1, self.customer_count + 1)]
        
        # Generate correlated data for realistic churn patterns
        # High-value customers tend to have better engagement and lower churn
        customer_values = np.random.lognormal(8, 1.5, self.customer_count)  # Revenue potential
        customer_values = np.clip(customer_values, 100, 50000)  # Realistic range
        
        # Generate correlated attributes
        data = []
        for i, customer_id in enumerate(customer_ids):
            # Correlate subscription type with value
            if customer_values[i] > 10000:
                subscription_type = random.choices(
                    ["Enterprise", "Premium"], 
                    weights=[0.7, 0.3]
                )[0]
                client_tier = "Enterprise"
            elif customer_values[i] > 3000:
                subscription_type = random.choices(
                    ["Premium", "Standard"], 
                    weights=[0.6, 0.4]
                )[0]
                client_tier = "SMB"
            else:
                subscription_type = random.choices(
                    ["Standard", "Basic"], 
                    weights=[0.7, 0.3]
                )[0]
                client_tier = "SMB"
            
            # Generate names
            first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Emily", 
                          "James", "Jessica", "William", "Ashley", "Richard", "Amanda", "Charles"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
                         "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
            
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            # Generate demographics
            age = random.randint(25, 65)
            gender = random.choice(["Male", "Female", "Other"])
            
            # Generate location data
            countries = ["United States", "Canada", "United Kingdom", "Germany", "France", "Australia", "Japan"]
            country = random.choice(countries)
            
            cities = {
                "United States": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
                "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
                "United Kingdom": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"],
                "Germany": ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"],
                "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
                "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
                "Japan": ["Tokyo", "Osaka", "Yokohama", "Nagoya", "Sapporo"]
            }
            city = random.choice(cities[country])
            
            # Generate account creation date (correlated with churn risk)
            # Older accounts tend to have lower churn risk
            days_ago = random.randint(30, 365)
            account_creation_date = self.end_date - timedelta(days=days_ago)
            
            # Generate status (correlated with engagement and value)
            # High-value, engaged customers are more likely to be active
            if customer_values[i] > 15000 and random.random() > 0.1:
                status = "Active"
            elif customer_values[i] > 5000 and random.random() > 0.3:
                status = "Active"
            elif random.random() > 0.6:
                status = "Active"
            else:
                status = random.choice(["At-Risk", "Inactive", "Churned"])
            
            # Generate contact information
            email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(['company.com', 'business.org', 'enterprise.net'])}"
            phone = f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            
            # Generate source system
            source_system = random.choice(["CRM_Salesforce", "Customer_Portal", "Marketing_Automation", "Sales_Team"])
            
            data.append({
                'customer_id': customer_id,
                'source_system_customer_id': f"SRC_{customer_id}",
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone_number': phone,
                'age': age,
                'gender': gender,
                'country': country,
                'city': city,
                'subscription_type': subscription_type,
                'account_creation_date': account_creation_date.strftime('%Y-%m-%d %H:%M:%S'),
                'status': status,
                'source_system': source_system,
                'ingestion_timestamp': self.end_date.strftime('%Y-%m-%d %H:%M:%S'),
                'raw_json_payload': f'{{"customer_value": {customer_values[i]:.2f}, "client_tier": "{client_tier}"}}'
            })
        
        df = pd.DataFrame(data)
        df.to_csv(self.data_dir / "raw_customer_demographics.csv", index=False)
        print(f"Generated {len(df)} customer records")
        return df
    
    def generate_transactions(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate transaction data correlated with customer profiles.
        
        Creates realistic transaction patterns where high-value customers
        have more frequent and larger transactions, while at-risk customers
        show declining transaction patterns.
        
        Args:
            customers_df: Customer demographics DataFrame
            
        Returns:
            pd.DataFrame: Transaction data with realistic patterns
        """
        print("Generating transaction data...")
        
        transactions = []
        customer_data = customers_df.set_index('customer_id')
        
        for customer_id, customer in customer_data.iterrows():
            # Determine transaction frequency based on customer value and status
            if customer['status'] == 'Active':
                if customer['subscription_type'] == 'Enterprise':
                    num_transactions = random.randint(20, 50)
                    avg_amount = random.uniform(2000, 8000)
                elif customer['subscription_type'] == 'Premium':
                    num_transactions = random.randint(10, 30)
                    avg_amount = random.uniform(500, 2000)
                else:
                    num_transactions = random.randint(5, 20)
                    avg_amount = random.uniform(100, 800)
            elif customer['status'] == 'At-Risk':
                num_transactions = random.randint(1, 8)
                avg_amount = random.uniform(50, 500)
            else:  # Inactive or Churned
                num_transactions = random.randint(0, 3)
                avg_amount = random.uniform(20, 200)
            
            # Generate transactions over time
            account_creation = datetime.strptime(customer['account_creation_date'], '%Y-%m-%d %H:%M:%S')
            days_since_creation = (self.end_date - account_creation).days
            
            for _ in range(num_transactions):
                # Transaction date (more recent for active customers)
                if customer['status'] == 'Active':
                    days_ago = random.randint(0, min(90, days_since_creation))
                elif customer['status'] == 'At-Risk':
                    days_ago = random.randint(30, min(180, days_since_creation))
                else:
                    days_ago = random.randint(min(60, days_since_creation), days_since_creation)
                
                transaction_date = self.end_date - timedelta(days=days_ago)
                
                # Transaction amount with some variation
                amount = max(0, np.random.normal(avg_amount, avg_amount * 0.3))
                
                # Payment method (correlated with customer tier)
                if customer['subscription_type'] == 'Enterprise':
                    payment_method = random.choices(
                        ["Credit Card", "Bank Transfer", "Invoice"], 
                        weights=[0.4, 0.4, 0.2]
                    )[0]
                else:
                    payment_method = random.choices(
                        ["Credit Card", "PayPal", "Bank Transfer"], 
                        weights=[0.6, 0.3, 0.1]
                    )[0]
                
                # Product information
                products = ["Software License", "Support Package", "Training", "Consulting", "Add-on Module"]
                product = random.choice(products)
                quantity = random.randint(1, 5)
                
                # Transaction type
                transaction_type = random.choices(
                    ["Purchase", "Subscription Payment", "Refund", "Upgrade"], 
                    weights=[0.7, 0.2, 0.05, 0.05]
                )[0]
                
                transactions.append({
                    'transaction_id': f"TXN_{len(transactions)+1:06d}",
                    'customer_id': customer_id,
                    'transaction_date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'amount': round(amount, 2),
                    'currency': 'USD',
                    'payment_method': payment_method,
                    'product_id': f"PROD_{random.randint(1000, 9999)}",
                    'product_name': product,
                    'quantity': quantity,
                    'transaction_type': transaction_type,
                    'source_system': random.choice(["Billing_Platform", "ECommerce_API", "Sales_System"]),
                    'ingestion_timestamp': self.end_date.strftime('%Y-%m-%d %H:%M:%S')
                })
        
        df = pd.DataFrame(transactions)
        df.to_csv(self.data_dir / "raw_transactions.csv", index=False)
        print(f"Generated {len(df)} transaction records")
        return df
    
    def generate_engagement_logs(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate engagement event logs with realistic patterns.
        
        Creates engagement events that correlate with customer health and churn risk.
        Active customers have more frequent and diverse engagement, while at-risk
        customers show declining engagement patterns.
        
        Args:
            customers_df: Customer demographics DataFrame
            
        Returns:
            pd.DataFrame: Engagement event logs with realistic patterns
        """
        print("Generating engagement logs...")
        
        events = []
        customer_data = customers_df.set_index('customer_id')
        
        # Event types with different engagement levels
        high_engagement_events = ["feature_usage", "dashboard_view", "report_generation", "api_call"]
        medium_engagement_events = ["page_view", "button_click", "form_submission", "search"]
        low_engagement_events = ["login", "logout", "page_view"]
        
        for customer_id, customer in customer_data.iterrows():
            # Determine engagement level based on customer status
            if customer['status'] == 'Active':
                if customer['subscription_type'] == 'Enterprise':
                    num_events = random.randint(100, 300)
                    engagement_level = "high"
                elif customer['subscription_type'] == 'Premium':
                    num_events = random.randint(50, 150)
                    engagement_level = "medium"
                else:
                    num_events = random.randint(20, 80)
                    engagement_level = "low"
            elif customer['status'] == 'At-Risk':
                num_events = random.randint(5, 30)
                engagement_level = "low"
            else:  # Inactive or Churned
                num_events = random.randint(0, 10)
                engagement_level = "low"
            
            # Generate events over time
            account_creation = datetime.strptime(customer['account_creation_date'], '%Y-%m-%d %H:%M:%S')
            days_since_creation = (self.end_date - account_creation).days
            
            for _ in range(num_events):
                # Event date (more recent for active customers)
                if customer['status'] == 'Active':
                    days_ago = random.randint(0, min(30, days_since_creation))
                elif customer['status'] == 'At-Risk':
                    days_ago = random.randint(15, min(90, days_since_creation))
                else:
                    days_ago = random.randint(min(30, days_since_creation), days_since_creation)
                
                event_date = self.end_date - timedelta(days=days_ago)
                
                # Select event type based on engagement level
                if engagement_level == "high":
                    all_events = high_engagement_events + medium_engagement_events + low_engagement_events
                    event_type = random.choices(
                        all_events,
                        weights=[0.4] * len(high_engagement_events) + [0.4] * len(medium_engagement_events) + [0.2] * len(low_engagement_events)
                    )[0]
                elif engagement_level == "medium":
                    medium_low_events = medium_engagement_events + low_engagement_events
                    event_type = random.choices(
                        medium_low_events,
                        weights=[0.6] * len(medium_engagement_events) + [0.4] * len(low_engagement_events)
                    )[0]
                else:
                    event_type = random.choice(low_engagement_events)
                
                # Device and browser information
                devices = ["Desktop", "Mobile", "Tablet"]
                browsers = ["Chrome", "Safari", "Firefox", "Edge"]
                operating_systems = ["Windows", "macOS", "iOS", "Android", "Linux"]
                
                device_type = random.choice(devices)
                browser = random.choice(browsers)
                os = random.choice(operating_systems)
                
                # Generate session ID (same for events within a day)
                session_id = f"SESS_{customer_id}_{event_date.strftime('%Y%m%d')}"
                
                # Page URL and feature usage
                pages = ["/dashboard", "/reports", "/settings", "/help", "/billing", "/profile"]
                features = ["analytics", "export", "filter", "search", "notification", "integration"]
                
                page_url = random.choice(pages)
                feature_used = random.choice(features) if event_type == "feature_usage" else None
                
                # Event data JSON
                event_data = {
                    "session_duration": random.randint(30, 1800),  # 30 seconds to 30 minutes
                    "page_load_time": random.uniform(0.5, 5.0),
                    "user_agent": f"Mozilla/5.0 ({os}) {browser}/91.0"
                }
                
                events.append({
                    'event_id': f"EVT_{len(events)+1:08d}",
                    'customer_id': customer_id,
                    'session_id': session_id,
                    'event_type': event_type,
                    'event_timestamp': event_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'device_type': device_type,
                    'browser': browser,
                    'operating_system': os,
                    'page_url': page_url,
                    'feature_used': feature_used,
                    'event_data_json': str(event_data),
                    'source_system': random.choice(["Web_Analytics", "App_Telemetry", "User_Tracking"]),
                    'ingestion_timestamp': self.end_date.strftime('%Y-%m-%d %H:%M:%S')
                })
        
        df = pd.DataFrame(events)
        df.to_csv(self.data_dir / "raw_engagement_logs.csv", index=False)
        print(f"Generated {len(df)} engagement events")
        return df
    
    def generate_support_interactions(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate support interaction data with realistic patterns.
        
        Creates support tickets that correlate with customer health and engagement.
        At-risk customers tend to have more support issues, while healthy customers
        have fewer but higher-quality support interactions.
        
        Args:
            customers_df: Customer demographics DataFrame
            
        Returns:
            pd.DataFrame: Support interaction data with realistic patterns
        """
        print("Generating support interactions...")
        
        interactions = []
        customer_data = customers_df.set_index('customer_id')
        
        for customer_id, customer in customer_data.iterrows():
            # Determine support ticket frequency based on customer status
            if customer['status'] == 'Active':
                num_tickets = random.randint(0, 5)
            elif customer['status'] == 'At-Risk':
                num_tickets = random.randint(2, 10)
            else:  # Inactive or Churned
                num_tickets = random.randint(1, 8)
            
            # Generate support tickets
            for _ in range(num_tickets):
                # Ticket creation date
                days_ago = random.randint(0, 180)
                created_at = self.end_date - timedelta(days=days_ago)
                
                # Interaction type and issue
                interaction_types = ["Chat", "Email", "Call", "Self-service"]
                issue_types = ["Bug Report", "Feature Request", "Billing Inquiry", "Technical Support", "Account Issue"]
                
                interaction_type = random.choice(interaction_types)
                issue_type = random.choice(issue_types)
                
                # Status and resolution
                if random.random() > 0.1:  # 90% resolved
                    status = "Resolved"
                    resolution_days = random.randint(1, 14)
                    resolved_at = created_at + timedelta(days=resolution_days)
                else:
                    status = random.choice(["Open", "In Progress"])
                    resolved_at = None
                
                # Satisfaction score (correlated with resolution and customer health)
                if status == "Resolved" and customer['status'] == 'Active':
                    satisfaction_score = random.choices([4, 5], weights=[0.3, 0.7])[0]
                elif status == "Resolved":
                    satisfaction_score = random.choices([3, 4, 5], weights=[0.4, 0.4, 0.2])[0]
                else:
                    satisfaction_score = random.choices([1, 2, 3], weights=[0.3, 0.4, 0.3])[0]
                
                # Agent ID
                agent_id = f"AGENT_{random.randint(100, 999)}"
                
                # Transcript text (simplified)
                transcript_samples = [
                    "Customer reported issue with login functionality. Provided troubleshooting steps.",
                    "Billing inquiry regarding recent charges. Explained pricing structure.",
                    "Feature request for additional reporting capabilities. Escalated to product team.",
                    "Technical support for integration issues. Provided API documentation.",
                    "Account access problem. Reset password and verified account status."
                ]
                transcript_text = random.choice(transcript_samples)
                
                interactions.append({
                    'ticket_id': f"TICKET_{len(interactions)+1:06d}",
                    'customer_id': customer_id,
                    'interaction_type': interaction_type,
                    'issue_type': issue_type,
                    'status': status,
                    'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'resolved_at': resolved_at.strftime('%Y-%m-%d %H:%M:%S') if resolved_at else None,
                    'agent_id': agent_id,
                    'satisfaction_score': satisfaction_score,
                    'transcript_text': transcript_text,
                    'source_system': random.choice(["Zendesk", "Intercom", "LiveChat", "Support_System"]),
                    'ingestion_timestamp': self.end_date.strftime('%Y-%m-%d %H:%M:%S')
                })
        
        df = pd.DataFrame(interactions)
        df.to_csv(self.data_dir / "raw_support_interactions.csv", index=False)
        print(f"Generated {len(df)} support interactions")
        return df
    
    def generate_feedback_surveys(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate survey feedback data with realistic NPS patterns.
        
        Creates survey responses that correlate with customer satisfaction and churn risk.
        Promoters (NPS 9-10) are less likely to churn, while detractors (NPS 0-6)
        have higher churn risk.
        
        Args:
            customers_df: Customer demographics DataFrame
            
        Returns:
            pd.DataFrame: Survey feedback data with realistic NPS patterns
        """
        print("Generating feedback surveys...")
        
        surveys = []
        customer_data = customers_df.set_index('customer_id')
        
        for customer_id, customer in customer_data.iterrows():
            # Determine survey frequency based on customer status
            if customer['status'] == 'Active':
                num_surveys = random.randint(1, 3)
            elif customer['status'] == 'At-Risk':
                num_surveys = random.randint(1, 2)
            else:  # Inactive or Churned
                num_surveys = random.randint(0, 2)
            
            # Generate survey responses
            for _ in range(num_surveys):
                # Survey date
                days_ago = random.randint(0, 90)
                response_date = self.end_date - timedelta(days=days_ago)
                
                # NPS score (correlated with customer status and satisfaction)
                if customer['status'] == 'Active':
                    nps_score = random.choices([9, 10, 8, 7], weights=[0.3, 0.3, 0.2, 0.2])[0]
                elif customer['status'] == 'At-Risk':
                    nps_score = random.choices([6, 7, 5, 4], weights=[0.3, 0.3, 0.2, 0.2])[0]
                else:  # Inactive or Churned
                    nps_score = random.choices([3, 4, 5, 2, 1], weights=[0.2, 0.2, 0.2, 0.2, 0.2])[0]
                
                # Survey type and questions
                survey_types = ["NPS", "Product Feedback", "Onboarding Survey", "Support Satisfaction"]
                survey_type = random.choice(survey_types)
                
                # Comments (correlated with NPS score)
                if nps_score >= 9:
                    comments = [
                        "Excellent product, very satisfied with the service.",
                        "Great experience, would definitely recommend.",
                        "Outstanding support and features.",
                        "Love the platform, very user-friendly."
                    ]
                elif nps_score >= 7:
                    comments = [
                        "Good product overall, some areas for improvement.",
                        "Satisfied with most features, minor issues.",
                        "Generally happy with the service.",
                        "Good platform with room for enhancement."
                    ]
                else:
                    comments = [
                        "Experiencing some issues with the platform.",
                        "Not fully satisfied with the current features.",
                        "Having trouble with support response times.",
                        "Product needs improvement in several areas."
                    ]
                
                comment = random.choice(comments)
                
                # Question details
                questions = [
                    "How likely are you to recommend our product?",
                    "What is your overall satisfaction with our service?",
                    "How would you rate our customer support?",
                    "What features would you like to see improved?"
                ]
                question_text = random.choice(questions)
                
                # Response text
                if nps_score >= 9:
                    response_text = "Very likely to recommend"
                elif nps_score >= 7:
                    response_text = "Somewhat likely to recommend"
                else:
                    response_text = "Not likely to recommend"
                
                surveys.append({
                    'survey_response_id': f"SURVEY_{len(surveys)+1:06d}",
                    'customer_id': customer_id,
                    'response_date': response_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'nps_score': nps_score,
                    'comments': comment,
                    'question_id': f"Q_{random.randint(1, 10)}",
                    'question_text': question_text,
                    'response_text': response_text,
                    'survey_type': survey_type,
                    'source_system': random.choice(["SurveyMonkey", "Qualtrics", "InApp_Survey", "Email_Survey"]),
                    'ingestion_timestamp': self.end_date.strftime('%Y-%m-%d %H:%M:%S')
                })
        
        df = pd.DataFrame(surveys)
        df.to_csv(self.data_dir / "raw_feedback_surveys.csv", index=False)
        print(f"Generated {len(df)} survey responses")
        return df
    
    def generate_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Generate all mock data for the A.U.R.A platform.
        
        Creates a complete dataset with correlated signals for testing the
        entire A.U.R.A pipeline from Bronze through Gold layers.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing all generated datasets
        """
        print("Starting A.U.R.A mock data generation...")
        print("=" * 50)
        
        # Generate all datasets
        customers = self.generate_customer_demographics()
        transactions = self.generate_transactions(customers)
        engagement = self.generate_engagement_logs(customers)
        support = self.generate_support_interactions(customers)
        surveys = self.generate_feedback_surveys(customers)
        
        print("=" * 50)
        print("Mock data generation completed!")
        print(f"Generated files in {self.data_dir}:")
        print("- raw_customer_demographics.csv")
        print("- raw_transactions.csv")
        print("- raw_engagement_logs.csv")
        print("- raw_support_interactions.csv")
        print("- raw_feedback_surveys.csv")
        
        return {
            'customers': customers,
            'transactions': transactions,
            'engagement': engagement,
            'support': support,
            'surveys': surveys
        }

def main():
    """Main function to generate mock data for A.U.R.A platform."""
    generator = MockDataGenerator()
    data = generator.generate_all_data()
    
    # Print summary statistics
    print("\nData Summary:")
    print(f"Customers: {len(data['customers'])}")
    print(f"Transactions: {len(data['transactions'])}")
    print(f"Engagement Events: {len(data['engagement'])}")
    print(f"Support Tickets: {len(data['support'])}")
    print(f"Survey Responses: {len(data['surveys'])}")
    
    # Print customer status distribution
    print("\nCustomer Status Distribution:")
    status_counts = data['customers']['status'].value_counts()
    for status, count in status_counts.items():
        print(f"  {status}: {count} ({count/len(data['customers'])*100:.1f}%)")

if __name__ == "__main__":
    main()
