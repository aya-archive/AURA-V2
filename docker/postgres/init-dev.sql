-- A.U.R.A - PostgreSQL Development Database Initialization
-- This script sets up the development database schema for A.U.R.A
-- Includes sample data and development-specific configurations

-- Create database extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Create development schema
CREATE SCHEMA IF NOT EXISTS aura_dev;

-- Set default search path
SET search_path TO aura_dev, public;

-- Create Bronze Layer Tables (Raw Data)
-- These tables store raw, unprocessed data as ingested from source systems

CREATE TABLE IF NOT EXISTS bronze_customers_raw (
    customer_id VARCHAR(255) PRIMARY KEY,
    source_system_customer_id VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(50),
    age INTEGER,
    gender VARCHAR(20),
    country VARCHAR(100),
    city VARCHAR(100),
    subscription_type VARCHAR(100),
    account_creation_date TIMESTAMP,
    status VARCHAR(50),
    source_system VARCHAR(100),
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_json_payload JSONB
);

CREATE TABLE IF NOT EXISTS bronze_transactions_raw (
    transaction_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255),
    transaction_date TIMESTAMP,
    amount DECIMAL(15,2),
    currency VARCHAR(10),
    payment_method VARCHAR(100),
    product_id VARCHAR(255),
    product_name VARCHAR(255),
    quantity INTEGER,
    transaction_type VARCHAR(100),
    source_system VARCHAR(100),
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bronze_engagement_events_raw (
    event_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255),
    session_id VARCHAR(255),
    event_type VARCHAR(100),
    event_timestamp TIMESTAMP,
    device_type VARCHAR(50),
    browser VARCHAR(100),
    operating_system VARCHAR(100),
    page_url TEXT,
    feature_used VARCHAR(255),
    event_data_json JSONB,
    source_system VARCHAR(100),
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Silver Layer Tables (Cleansed Data)
-- These tables contain cleaned, standardized, and enriched data

CREATE TABLE IF NOT EXISTS silver_customer_dim (
    customer_pk VARCHAR(255) PRIMARY KEY,
    source_customer_id VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email_address VARCHAR(255),
    age_group VARCHAR(20),
    gender_standardized VARCHAR(20),
    country VARCHAR(100),
    region VARCHAR(100),
    industry VARCHAR(100),
    current_subscription_plan VARCHAR(100),
    account_creation_date DATE,
    last_active_date DATE,
    account_status_standardized VARCHAR(50),
    total_lifetime_revenue DECIMAL(15,2),
    average_transaction_value DECIMAL(15,2),
    total_support_tickets_lifetime INTEGER,
    avg_satisfaction_score_lifetime DECIMAL(3,2),
    most_recent_nps_score INTEGER,
    data_last_processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver_transaction_facts_daily (
    transaction_date DATE,
    customer_pk VARCHAR(255),
    total_revenue_daily DECIMAL(15,2),
    total_transactions_daily INTEGER,
    distinct_products_purchased_daily INTEGER,
    avg_item_price_daily DECIMAL(15,2),
    refund_count_daily INTEGER,
    PRIMARY KEY (transaction_date, customer_pk),
    FOREIGN KEY (customer_pk) REFERENCES silver_customer_dim(customer_pk)
);

-- Create Gold Layer Tables (Business-Ready Data)
-- These tables contain aggregated, business-ready datasets for dashboards and AI models

CREATE TABLE IF NOT EXISTS gold_customer_360_dashboard_view (
    customer_pk VARCHAR(255) PRIMARY KEY,
    customer_name VARCHAR(255),
    email_address VARCHAR(255),
    subscription_plan VARCHAR(100),
    account_status VARCHAR(50),
    days_since_signup INTEGER,
    current_health_score DECIMAL(5,2),
    churn_risk_level VARCHAR(20),
    predicted_churn_probability DECIMAL(5,4),
    recommended_action VARCHAR(255),
    upsell_opportunity_flag BOOLEAN,
    cross_sell_opportunity_flag BOOLEAN,
    last_active_date DATE,
    MRR_current_month DECIMAL(15,2),
    YOY_MRR_growth_percentage DECIMAL(5,2),
    avg_engagement_score_90d DECIMAL(5,2),
    last_nps_score INTEGER,
    open_support_tickets_count INTEGER,
    client_segment VARCHAR(100),
    dashboard_data_last_refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gold_ai_model_features_for_churn_prediction (
    customer_pk VARCHAR(255),
    feature_snapshot_date DATE,
    feature_avg_daily_active_events_90d DECIMAL(10,2),
    feature_total_transaction_value_60d DECIMAL(15,2),
    feature_support_tickets_30d_count INTEGER,
    feature_days_since_last_login INTEGER,
    feature_last_nps_score INTEGER,
    feature_churn_history_365d_flag BOOLEAN,
    feature_subscription_plan_tier INTEGER,
    feature_age_of_account_days INTEGER,
    target_churned_next_30d BOOLEAN,
    PRIMARY KEY (customer_pk, feature_snapshot_date)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_bronze_customers_customer_id ON bronze_customers_raw(customer_id);
CREATE INDEX IF NOT EXISTS idx_bronze_transactions_customer_id ON bronze_transactions_raw(customer_id);
CREATE INDEX IF NOT EXISTS idx_bronze_transactions_date ON bronze_transactions_raw(transaction_date);
CREATE INDEX IF NOT EXISTS idx_bronze_engagement_customer_id ON bronze_engagement_events_raw(customer_id);
CREATE INDEX IF NOT EXISTS idx_bronze_engagement_timestamp ON bronze_engagement_events_raw(event_timestamp);

CREATE INDEX IF NOT EXISTS idx_silver_customer_pk ON silver_customer_dim(customer_pk);
CREATE INDEX IF NOT EXISTS idx_silver_transaction_date ON silver_transaction_facts_daily(transaction_date);
CREATE INDEX IF NOT EXISTS idx_silver_transaction_customer ON silver_transaction_facts_daily(customer_pk);

CREATE INDEX IF NOT EXISTS idx_gold_customer_health ON gold_customer_360_dashboard_view(current_health_score);
CREATE INDEX IF NOT EXISTS idx_gold_churn_risk ON gold_customer_360_dashboard_view(churn_risk_level);
CREATE INDEX IF NOT EXISTS idx_gold_features_date ON gold_ai_model_features_for_churn_prediction(feature_snapshot_date);

-- Create views for common queries
CREATE OR REPLACE VIEW customer_health_summary AS
SELECT 
    churn_risk_level,
    COUNT(*) as customer_count,
    AVG(current_health_score) as avg_health_score,
    AVG(predicted_churn_probability) as avg_churn_probability
FROM gold_customer_360_dashboard_view
GROUP BY churn_risk_level;

CREATE OR REPLACE VIEW daily_metrics AS
SELECT 
    transaction_date,
    COUNT(DISTINCT customer_pk) as active_customers,
    SUM(total_revenue_daily) as total_daily_revenue,
    AVG(total_revenue_daily) as avg_customer_revenue
FROM silver_transaction_facts_daily
GROUP BY transaction_date
ORDER BY transaction_date DESC;

-- Grant permissions for development
GRANT ALL PRIVILEGES ON SCHEMA aura_dev TO aura_dev_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA aura_dev TO aura_dev_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA aura_dev TO aura_dev_user;
