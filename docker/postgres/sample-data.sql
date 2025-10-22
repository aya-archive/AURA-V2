-- A.U.R.A - Sample Data for Development
-- This script populates the development database with sample data
-- to enable testing and development of the A.U.R.A platform

-- Set search path
SET search_path TO aura_dev, public;

-- Insert sample customers into Bronze layer
INSERT INTO bronze_customers_raw (
    customer_id, source_system_customer_id, first_name, last_name, email, 
    phone_number, age, gender, country, city, subscription_type, 
    account_creation_date, status, source_system
) VALUES 
('CUST001', 'SF_001', 'John', 'Smith', 'john.smith@techcorp.com', '+1-555-0101', 35, 'Male', 'United States', 'San Francisco', 'Premium', '2023-01-15 10:30:00', 'Active', 'CRM_Salesforce'),
('CUST002', 'SF_002', 'Sarah', 'Johnson', 'sarah.johnson@innovate.com', '+1-555-0102', 28, 'Female', 'United States', 'New York', 'Enterprise', '2023-02-20 14:15:00', 'Active', 'CRM_Salesforce'),
('CUST003', 'SF_003', 'Michael', 'Brown', 'michael.brown@startup.io', '+1-555-0103', 42, 'Male', 'Canada', 'Toronto', 'Basic', '2023-03-10 09:45:00', 'At Risk', 'CRM_Salesforce'),
('CUST004', 'SF_004', 'Emily', 'Davis', 'emily.davis@enterprise.com', '+1-555-0104', 31, 'Female', 'United Kingdom', 'London', 'Enterprise', '2023-01-25 16:20:00', 'Active', 'CRM_Salesforce'),
('CUST005', 'SF_005', 'David', 'Wilson', 'david.wilson@smallbiz.com', '+1-555-0105', 29, 'Male', 'Australia', 'Sydney', 'Basic', '2023-04-05 11:30:00', 'Churned', 'CRM_Salesforce'),
('CUST006', 'SF_006', 'Lisa', 'Anderson', 'lisa.anderson@techstart.com', '+1-555-0106', 26, 'Female', 'United States', 'Austin', 'Premium', '2023-02-14 13:45:00', 'Active', 'CRM_Salesforce'),
('CUST007', 'SF_007', 'Robert', 'Taylor', 'robert.taylor@corp.com', '+1-555-0107', 45, 'Male', 'Germany', 'Berlin', 'Enterprise', '2023-01-08 08:15:00', 'Active', 'CRM_Salesforce'),
('CUST008', 'SF_008', 'Jennifer', 'Martinez', 'jennifer.martinez@startup.com', '+1-555-0108', 33, 'Female', 'Spain', 'Madrid', 'Premium', '2023-03-22 15:30:00', 'At Risk', 'CRM_Salesforce'),
('CUST009', 'SF_009', 'James', 'Garcia', 'james.garcia@business.com', '+1-555-0109', 38, 'Male', 'France', 'Paris', 'Enterprise', '2023-02-01 12:00:00', 'Active', 'CRM_Salesforce'),
('CUST010', 'SF_010', 'Maria', 'Rodriguez', 'maria.rodriguez@company.com', '+1-555-0110', 27, 'Female', 'Brazil', 'São Paulo', 'Basic', '2023-04-12 14:45:00', 'Trial', 'CRM_Salesforce');

-- Insert sample transactions
INSERT INTO bronze_transactions_raw (
    transaction_id, customer_id, transaction_date, amount, currency, 
    payment_method, product_id, product_name, quantity, transaction_type, source_system
) VALUES 
('TXN001', 'CUST001', '2023-01-15 10:35:00', 99.00, 'USD', 'Credit Card', 'PROD001', 'Premium Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN002', 'CUST001', '2023-02-15 10:35:00', 99.00, 'USD', 'Credit Card', 'PROD001', 'Premium Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN003', 'CUST001', '2023-03-15 10:35:00', 99.00, 'USD', 'Credit Card', 'PROD001', 'Premium Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN004', 'CUST002', '2023-02-20 14:20:00', 299.00, 'USD', 'Credit Card', 'PROD002', 'Enterprise Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN005', 'CUST002', '2023-03-20 14:20:00', 299.00, 'USD', 'Credit Card', 'PROD002', 'Enterprise Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN006', 'CUST003', '2023-03-10 09:50:00', 29.00, 'CAD', 'PayPal', 'PROD003', 'Basic Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN007', 'CUST004', '2023-01-25 16:25:00', 299.00, 'GBP', 'Bank Transfer', 'PROD002', 'Enterprise Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN008', 'CUST004', '2023-02-25 16:25:00', 299.00, 'GBP', 'Bank Transfer', 'PROD002', 'Enterprise Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN009', 'CUST004', '2023-03-25 16:25:00', 299.00, 'GBP', 'Bank Transfer', 'PROD002', 'Enterprise Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN010', 'CUST005', '2023-04-05 11:35:00', 29.00, 'AUD', 'Credit Card', 'PROD003', 'Basic Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN011', 'CUST006', '2023-02-14 13:50:00', 99.00, 'USD', 'Credit Card', 'PROD001', 'Premium Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN012', 'CUST006', '2023-03-14 13:50:00', 99.00, 'USD', 'Credit Card', 'PROD001', 'Premium Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN013', 'CUST007', '2023-01-08 08:20:00', 299.00, 'EUR', 'Credit Card', 'PROD002', 'Enterprise Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN014', 'CUST007', '2023-02-08 08:20:00', 299.00, 'EUR', 'Credit Card', 'PROD002', 'Enterprise Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN015', 'CUST007', '2023-03-08 08:20:00', 299.00, 'EUR', 'Credit Card', 'PROD002', 'Enterprise Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN016', 'CUST008', '2023-03-22 15:35:00', 99.00, 'EUR', 'PayPal', 'PROD001', 'Premium Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN017', 'CUST009', '2023-02-01 12:05:00', 299.00, 'EUR', 'Bank Transfer', 'PROD002', 'Enterprise Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN018', 'CUST009', '2023-03-01 12:05:00', 299.00, 'EUR', 'Bank Transfer', 'PROD002', 'Enterprise Plan', 1, 'Subscription Payment', 'Billing_Platform'),
('TXN019', 'CUST010', '2023-04-12 14:50:00', 0.00, 'BRL', 'Credit Card', 'PROD003', 'Basic Plan', 1, 'Trial', 'Billing_Platform');

-- Insert sample engagement events
INSERT INTO bronze_engagement_events_raw (
    event_id, customer_id, session_id, event_type, event_timestamp, 
    device_type, browser, operating_system, page_url, feature_used, source_system
) VALUES 
('EVT001', 'CUST001', 'SESS001', 'login', '2023-04-01 09:00:00', 'Desktop', 'Chrome', 'Windows', '/dashboard', 'authentication', 'Web_Analytics'),
('EVT002', 'CUST001', 'SESS001', 'feature_usage', '2023-04-01 09:05:00', 'Desktop', 'Chrome', 'Windows', '/analytics', 'analytics_dashboard', 'Web_Analytics'),
('EVT003', 'CUST001', 'SESS001', 'feature_usage', '2023-04-01 09:10:00', 'Desktop', 'Chrome', 'Windows', '/reports', 'report_generator', 'Web_Analytics'),
('EVT004', 'CUST001', 'SESS001', 'logout', '2023-04-01 09:30:00', 'Desktop', 'Chrome', 'Windows', '/dashboard', 'authentication', 'Web_Analytics'),
('EVT005', 'CUST002', 'SESS002', 'login', '2023-04-01 10:00:00', 'Desktop', 'Safari', 'macOS', '/dashboard', 'authentication', 'Web_Analytics'),
('EVT006', 'CUST002', 'SESS002', 'feature_usage', '2023-04-01 10:05:00', 'Desktop', 'Safari', 'macOS', '/analytics', 'analytics_dashboard', 'Web_Analytics'),
('EVT007', 'CUST002', 'SESS002', 'feature_usage', '2023-04-01 10:15:00', 'Desktop', 'Safari', 'macOS', '/api', 'api_access', 'Web_Analytics'),
('EVT008', 'CUST003', 'SESS003', 'login', '2023-04-01 11:00:00', 'Mobile', 'Chrome', 'Android', '/dashboard', 'authentication', 'App_Telemetry'),
('EVT009', 'CUST003', 'SESS003', 'feature_usage', '2023-04-01 11:05:00', 'Mobile', 'Chrome', 'Android', '/mobile', 'mobile_app', 'App_Telemetry'),
('EVT010', 'CUST004', 'SESS004', 'login', '2023-04-01 12:00:00', 'Desktop', 'Firefox', 'Windows', '/dashboard', 'authentication', 'Web_Analytics'),
('EVT011', 'CUST004', 'SESS004', 'feature_usage', '2023-04-01 12:05:00', 'Desktop', 'Firefox', 'Windows', '/analytics', 'analytics_dashboard', 'Web_Analytics'),
('EVT012', 'CUST004', 'SESS004', 'feature_usage', '2023-04-01 12:10:00', 'Desktop', 'Firefox', 'Windows', '/integrations', 'third_party_integration', 'Web_Analytics'),
('EVT013', 'CUST005', 'SESS005', 'login', '2023-03-25 14:00:00', 'Desktop', 'Chrome', 'Windows', '/dashboard', 'authentication', 'Web_Analytics'),
('EVT014', 'CUST005', 'SESS005', 'feature_usage', '2023-03-25 14:05:00', 'Desktop', 'Chrome', 'Windows', '/analytics', 'analytics_dashboard', 'Web_Analytics'),
('EVT015', 'CUST006', 'SESS006', 'login', '2023-04-01 15:00:00', 'Desktop', 'Chrome', 'Windows', '/dashboard', 'authentication', 'Web_Analytics'),
('EVT016', 'CUST006', 'SESS006', 'feature_usage', '2023-04-01 15:05:00', 'Desktop', 'Chrome', 'Windows', '/analytics', 'analytics_dashboard', 'Web_Analytics'),
('EVT017', 'CUST006', 'SESS006', 'feature_usage', '2023-04-01 15:10:00', 'Desktop', 'Chrome', 'Windows', '/reports', 'report_generator', 'Web_Analytics'),
('EVT018', 'CUST007', 'SESS007', 'login', '2023-04-01 16:00:00', 'Desktop', 'Safari', 'macOS', '/dashboard', 'authentication', 'Web_Analytics'),
('EVT019', 'CUST007', 'SESS007', 'feature_usage', '2023-04-01 16:05:00', 'Desktop', 'Safari', 'macOS', '/analytics', 'analytics_dashboard', 'Web_Analytics'),
('EVT020', 'CUST008', 'SESS008', 'login', '2023-04-01 17:00:00', 'Mobile', 'Safari', 'iOS', '/dashboard', 'authentication', 'App_Telemetry');

-- Insert sample data into Silver layer (processed/cleansed data)
INSERT INTO silver_customer_dim (
    customer_pk, source_customer_id, first_name, last_name, email_address,
    age_group, gender_standardized, country, region, industry,
    current_subscription_plan, account_creation_date, last_active_date,
    account_status_standardized, total_lifetime_revenue, average_transaction_value,
    total_support_tickets_lifetime, avg_satisfaction_score_lifetime, most_recent_nps_score
) VALUES 
('CUST001', 'CUST001', 'John', 'Smith', 'john.smith@techcorp.com', '30-39', 'Male', 'United States', 'North America', 'Technology', 'Premium', '2023-01-15', '2023-04-01', 'Active', 297.00, 99.00, 2, 4.5, 8),
('CUST002', 'CUST002', 'Sarah', 'Johnson', 'sarah.johnson@innovate.com', '25-34', 'Female', 'United States', 'North America', 'Technology', 'Enterprise', '2023-02-20', '2023-04-01', 'Active', 598.00, 299.00, 1, 4.8, 9),
('CUST003', 'CUST003', 'Michael', 'Brown', 'michael.brown@startup.io', '40-49', 'Male', 'Canada', 'North America', 'Technology', 'Basic', '2023-03-10', '2023-04-01', 'At Risk', 29.00, 29.00, 3, 3.2, 6),
('CUST004', 'CUST004', 'Emily', 'Davis', 'emily.davis@enterprise.com', '30-39', 'Female', 'United Kingdom', 'Europe', 'Enterprise', 'Enterprise', '2023-01-25', '2023-04-01', 'Active', 897.00, 299.00, 1, 4.7, 8),
('CUST005', 'CUST005', 'David', 'Wilson', 'david.wilson@smallbiz.com', '25-34', 'Male', 'Australia', 'Asia Pacific', 'Small Business', 'Basic', '2023-04-05', '2023-03-25', 'Churned', 29.00, 29.00, 5, 2.1, 3),
('CUST006', 'CUST006', 'Lisa', 'Anderson', 'lisa.anderson@techstart.com', '25-34', 'Female', 'United States', 'North America', 'Technology', 'Premium', '2023-02-14', '2023-04-01', 'Active', 198.00, 99.00, 1, 4.6, 8),
('CUST007', 'CUST007', 'Robert', 'Taylor', 'robert.taylor@corp.com', '40-49', 'Male', 'Germany', 'Europe', 'Enterprise', 'Enterprise', '2023-01-08', '2023-04-01', 'Active', 897.00, 299.00, 0, 4.9, 9),
('CUST008', 'CUST008', 'Jennifer', 'Martinez', 'jennifer.martinez@startup.com', '30-39', 'Female', 'Spain', 'Europe', 'Technology', 'Premium', '2023-03-22', '2023-04-01', 'At Risk', 99.00, 99.00, 2, 3.8, 7),
('CUST009', 'CUST009', 'James', 'Garcia', 'james.garcia@business.com', '35-44', 'Male', 'France', 'Europe', 'Enterprise', 'Enterprise', '2023-02-01', '2023-04-01', 'Active', 598.00, 299.00, 1, 4.4, 8),
('CUST010', 'CUST010', 'Maria', 'Rodriguez', 'maria.rodriguez@company.com', '25-34', 'Female', 'Brazil', 'South America', 'Small Business', 'Basic', '2023-04-12', '2023-04-12', 'Trial', 0.00, 0.00, 0, 0.0, 0);

-- Insert sample data into Gold layer (business-ready aggregated data)
INSERT INTO gold_customer_360_dashboard_view (
    customer_pk, customer_name, email_address, subscription_plan, account_status,
    days_since_signup, current_health_score, churn_risk_level, predicted_churn_probability,
    recommended_action, upsell_opportunity_flag, cross_sell_opportunity_flag,
    last_active_date, MRR_current_month, YOY_MRR_growth_percentage,
    avg_engagement_score_90d, last_nps_score, open_support_tickets_count, client_segment
) VALUES 
('CUST001', 'John Smith', 'john.smith@techcorp.com', 'Premium', 'Active', 76, 85.5, 'Low', 0.12, 'Continue monitoring', false, true, '2023-04-01', 99.00, 15.2, 8.5, 8, 0, 'High-Value'),
('CUST002', 'Sarah Johnson', 'sarah.johnson@innovate.com', 'Enterprise', 'Active', 40, 92.3, 'Low', 0.08, 'Continue monitoring', true, false, '2023-04-01', 299.00, 25.8, 9.2, 9, 0, 'Enterprise'),
('CUST003', 'Michael Brown', 'michael.brown@startup.io', 'Basic', 'At Risk', 22, 45.2, 'High', 0.78, 'Schedule retention call', false, false, '2023-04-01', 29.00, -10.5, 3.2, 6, 1, 'At-Risk'),
('CUST004', 'Emily Davis', 'emily.davis@enterprise.com', 'Enterprise', 'Active', 66, 88.7, 'Low', 0.15, 'Continue monitoring', false, true, '2023-04-01', 299.00, 18.3, 8.8, 8, 0, 'Enterprise'),
('CUST005', 'David Wilson', 'david.wilson@smallbiz.com', 'Basic', 'Churned', 0, 25.1, 'High', 0.95, 'Win-back campaign', false, false, '2023-03-25', 0.00, -100.0, 2.1, 3, 0, 'Churned'),
('CUST006', 'Lisa Anderson', 'lisa.anderson@techstart.com', 'Premium', 'Active', 46, 82.1, 'Medium', 0.35, 'Proactive check-in', true, false, '2023-04-01', 99.00, 12.7, 7.8, 8, 0, 'High-Value'),
('CUST007', 'Robert Taylor', 'robert.taylor@corp.com', 'Enterprise', 'Active', 83, 95.8, 'Low', 0.05, 'Continue monitoring', false, true, '2023-04-01', 299.00, 22.1, 9.5, 9, 0, 'Enterprise'),
('CUST008', 'Jennifer Martinez', 'jennifer.martinez@startup.com', 'Premium', 'At Risk', 10, 52.3, 'High', 0.65, 'Schedule retention call', false, false, '2023-04-01', 99.00, 5.2, 4.1, 7, 1, 'At-Risk'),
('CUST009', 'James Garcia', 'james.garcia@business.com', 'Enterprise', 'Active', 59, 87.4, 'Low', 0.18, 'Continue monitoring', false, true, '2023-04-01', 299.00, 20.3, 8.2, 8, 0, 'Enterprise'),
('CUST010', 'Maria Rodriguez', 'maria.rodriguez@company.com', 'Basic', 'Trial', 0, 60.0, 'Medium', 0.45, 'Onboarding support', true, false, '2023-04-12', 0.00, 0.0, 6.0, 0, 0, 'New Customer');

-- Insert sample AI model features
INSERT INTO gold_ai_model_features_for_churn_prediction (
    customer_pk, feature_snapshot_date, feature_avg_daily_active_events_90d,
    feature_total_transaction_value_60d, feature_support_tickets_30d_count,
    feature_days_since_last_login, feature_last_nps_score, feature_churn_history_365d_flag,
    feature_subscription_plan_tier, feature_age_of_account_days, target_churned_next_30d
) VALUES 
('CUST001', '2023-04-01', 8.5, 198.00, 0, 0, 8, false, 2, 76, false),
('CUST002', '2023-04-01', 9.2, 598.00, 0, 0, 9, false, 3, 40, false),
('CUST003', '2023-04-01', 3.2, 29.00, 2, 0, 6, false, 1, 22, true),
('CUST004', '2023-04-01', 8.8, 897.00, 0, 0, 8, false, 3, 66, false),
('CUST005', '2023-04-01', 2.1, 29.00, 3, 7, 3, false, 1, 0, true),
('CUST006', '2023-04-01', 7.8, 198.00, 0, 0, 8, false, 2, 46, false),
('CUST007', '2023-04-01', 9.5, 897.00, 0, 0, 9, false, 3, 83, false),
('CUST008', '2023-04-01', 4.1, 99.00, 1, 0, 7, false, 2, 10, true),
('CUST009', '2023-04-01', 8.2, 598.00, 0, 0, 8, false, 3, 59, false),
('CUST010', '2023-04-01', 6.0, 0.00, 0, 0, 0, false, 1, 0, false);

-- Update statistics
ANALYZE;
