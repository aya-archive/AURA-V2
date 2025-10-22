# A.U.R.A (Adaptive User Retention Assistant) - Application Constants
# This module contains all global constants, thresholds, and fixed values
# used throughout the A.U.R.A platform for consistent behavior

from typing import Dict, List, Tuple
from enum import Enum

# Color palette for A.U.R.A dashboard and visualizations
# These colors are used consistently across all UI components to maintain brand identity
class Colors:
    """A.U.R.A brand colors and semantic colors for dashboard visualizations."""
    
    # Primary brand colors
    AURA_BLUE_DEEP = "#004D7A"      # Core brand identity, primary actions
    AURA_BLUE_LIGHT = "#E0EFF7"     # Backgrounds, secondary containers
    AURA_TEAL = "#00B3B3"           # Call-to-action buttons, interactive elements
    AURA_ORANGE = "#FF8C00"         # Secondary accents, highlights
    
    # Neutral colors
    DARK_GRAY = "#333333"           # Primary body text, headings
    MEDIUM_GRAY = "#666666"         # Secondary text, icons, borders
    LIGHT_GRAY = "#F8F8F8"         # Default background for content areas
    OFF_WHITE = "#FFFFFF"          # Card backgrounds, main page backgrounds
    
    # Semantic colors for data visualization
    SUCCESS = "#28A745"            # Positive trends, healthy clients, successful actions
    WARNING = "#FFC107"             # At-risk clients, pending actions, moderate issues
    ERROR = "#DC3545"              # Churn risk (high), critical errors, negative trends
    INFO = "#17A2B8"               # General information, tips, neutral data points

# Typography settings for consistent text styling
class Typography:
    """Typography settings for A.U.R.A dashboard and components."""
    
    # Font family
    FONT_FAMILY = "Lato, Arial, sans-serif"
    
    # Font sizes (in rem)
    H1_SIZE = "2.5rem"    # Page titles
    H2_SIZE = "2rem"      # Section titles  
    H3_SIZE = "1.5rem"    # Card titles/sub-sections
    H4_SIZE = "1.25rem"   # Widget titles
    BODY_SIZE = "1rem"    # Body text
    SUBTITLE_SIZE = "1.125rem"  # Subtitle/lead text
    CAPTION_SIZE = "0.875rem"   # Caption/small text
    DATA_LABEL_SIZE = "0.75rem" # Data labels/tooltips
    
    # Font weights
    LIGHT = "300"
    REGULAR = "400" 
    MEDIUM = "500"
    BOLD = "700"
    
    # Line heights
    BODY_LINE_HEIGHT = "1.5"
    HEADING_LINE_HEIGHT = "1.2"

# Churn risk classification thresholds
# These thresholds determine how clients are classified for churn risk
class ChurnRiskThresholds:
    """Thresholds for classifying client churn risk levels."""
    
    # Health score thresholds (0-100 scale)
    HEALTH_SCORE_EXCELLENT = 80    # Excellent health - low churn risk
    HEALTH_SCORE_GOOD = 60         # Good health - medium churn risk  
    HEALTH_SCORE_FAIR = 40         # Fair health - high churn risk
    HEALTH_SCORE_POOR = 20         # Poor health - very high churn risk
    
    # Engagement score thresholds (0-1 scale)
    ENGAGEMENT_HIGH = 0.8          # High engagement - low churn risk
    ENGAGEMENT_MEDIUM = 0.5        # Medium engagement - medium churn risk
    ENGAGEMENT_LOW = 0.3           # Low engagement - high churn risk
    
    # Days since last activity thresholds
    DAYS_SINCE_ACTIVE_RECENT = 7   # Recent activity - low churn risk
    DAYS_SINCE_ACTIVE_MODERATE = 30 # Moderate activity - medium churn risk
    DAYS_SINCE_ACTIVE_OLD = 90     # Old activity - high churn risk
    
    # NPS score thresholds
    NPS_PROMOTER = 9               # Promoter - low churn risk
    NPS_PASSIVE = 7                # Passive - medium churn risk
    NPS_DETRACTOR = 6              # Detractor - high churn risk

# Client segmentation categories
# These categories help organize clients for targeted retention strategies
class ClientSegments:
    """Client segmentation categories for targeted retention strategies."""
    
    # Client tiers based on revenue
    SMB = "SMB"                    # Small and medium business
    ENTERPRISE = "Enterprise"      # Large enterprise clients
    STARTUP = "Startup"           # Early-stage companies
    
    # Client health categories
    HEALTHY = "Healthy"           # Low churn risk, high engagement
    AT_RISK = "At-Risk"          # Medium churn risk, declining engagement
    CRITICAL = "Critical"        # High churn risk, very low engagement
    CHURNED = "Churned"          # Already churned clients
    
    # Client value categories
    HIGH_VALUE = "High-Value"     # High revenue clients
    MEDIUM_VALUE = "Medium-Value" # Medium revenue clients
    LOW_VALUE = "Low-Value"      # Low revenue clients

# Retention strategy categories
# These categories organize retention strategies by type and target
class StrategyCategories:
    """Categories for organizing retention strategies."""
    
    CHURN_PREVENTION = "Churn Prevention"    # Strategies to prevent churn
    ENGAGEMENT_BOOST = "Engagement Boost"   # Strategies to increase engagement
    UPSELL = "Upsell"                       # Strategies to increase revenue
    ONBOARDING = "Onboarding"              # Strategies for new clients
    SUPPORT = "Support"                     # Strategies for support issues

# AI Model parameters and thresholds
# These parameters control the behavior of AI models and decision engines
class AIModelParams:
    """Parameters for AI models and decision engines."""
    
    # Prophet forecasting parameters
    PROPHET_DAILY_SEASONALITY = True        # Enable daily seasonality in forecasts
    PROPHET_WEEKLY_SEASONALITY = True      # Enable weekly seasonality in forecasts
    PROPHET_YEARLY_SEASONALITY = True      # Enable yearly seasonality in forecasts
    PROPHET_CHANGEPOINT_PRIOR_SCALE = 0.05 # Sensitivity to trend changes
    
    # Decision engine rule weights
    RULE_WEIGHTS = {
        "engagement": 0.4,      # 40% weight for engagement metrics
        "revenue": 0.3,          # 30% weight for revenue metrics
        "support": 0.2,         # 20% weight for support interactions
        "nps": 0.1              # 10% weight for NPS scores
    }
    
    # Chatbot parameters
    CHATBOT_MAX_CONTEXT_LENGTH = 4000       # Maximum context length for chatbot
    CHATBOT_TEMPERATURE = 0.7              # Temperature for response generation
    CHATBOT_MAX_TOKENS = 500               # Maximum tokens for responses

# Dashboard configuration constants
# These constants control the layout and behavior of the dashboard
class DashboardConfig:
    """Configuration constants for the A.U.R.A dashboard."""
    
    # Page configuration
    PAGE_TITLE = "A.U.R.A - AI Retention Analytics"
    PAGE_ICON = "🤖"
    LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
    
    # Data refresh intervals (in seconds)
    DATA_REFRESH_INTERVAL = 300           # 5 minutes for real-time data
    CHART_UPDATE_INTERVAL = 60            # 1 minute for chart updates
    
    # Pagination settings
    CLIENTS_PER_PAGE = 25                 # Number of clients per page
    MAX_CLIENTS_DISPLAY = 1000            # Maximum clients to display
    
    # Chart configuration
    CHART_HEIGHT = 400                    # Default chart height
    CHART_WIDTH = "100%"                 # Default chart width
    CHART_THEME = "plotly_white"         # Default chart theme

# File paths and naming conventions
# These constants define standard file paths and naming conventions
class FilePaths:
    """Standard file paths and naming conventions for A.U.R.A platform."""
    
    # Data file naming patterns
    BRONZE_PREFIX = "raw_"               # Prefix for Bronze layer files
    SILVER_PREFIX = "processed_"         # Prefix for Silver layer files
    GOLD_PREFIX = "aggregated_"          # Prefix for Gold layer files
    
    # Model file extensions
    MODEL_EXTENSION = ".joblib"          # Extension for saved models
    CONFIG_EXTENSION = ".json"           # Extension for model configurations
    
    # Log file patterns
    LOG_PREFIX = "aura_"                  # Prefix for log files
    LOG_EXTENSION = ".log"               # Extension for log files

# API endpoints and routes
# These constants define API routes for the A.U.R.A platform
class APIRoutes:
    """API routes and endpoints for A.U.R.A platform."""
    
    # Base API path
    API_PREFIX = "/api/v1"
    
    # Data endpoints
    DATA_BRONZE = f"{API_PREFIX}/data/bronze"
    DATA_SILVER = f"{API_PREFIX}/data/silver"
    DATA_GOLD = f"{API_PREFIX}/data/gold"
    
    # Model endpoints
    MODEL_FORECAST = f"{API_PREFIX}/model/forecast"
    MODEL_PREDICT = f"{API_PREFIX}/model/predict"
    MODEL_CHATBOT = f"{API_PREFIX}/model/chatbot"
    
    # Dashboard endpoints
    DASHBOARD_KPIS = f"{API_PREFIX}/dashboard/kpis"
    DASHBOARD_CLIENTS = f"{API_PREFIX}/dashboard/clients"

# Error messages and validation rules
# These constants define error messages and validation rules
class ValidationRules:
    """Validation rules and error messages for A.U.R.A platform."""
    
    # Data validation rules
    MIN_CUSTOMER_ID_LENGTH = 1           # Minimum customer ID length
    MAX_CUSTOMER_ID_LENGTH = 50          # Maximum customer ID length
    MIN_EMAIL_LENGTH = 5                # Minimum email length
    MAX_EMAIL_LENGTH = 100               # Maximum email length
    
    # Error messages
    INVALID_CUSTOMER_ID = "Invalid customer ID format"
    INVALID_EMAIL = "Invalid email format"
    MISSING_REQUIRED_FIELD = "Required field is missing"
    DATA_VALIDATION_ERROR = "Data validation failed"
    
    # Success messages
    DATA_SAVED_SUCCESS = "Data saved successfully"
    MODEL_TRAINED_SUCCESS = "Model trained successfully"
    PREDICTION_SUCCESS = "Prediction completed successfully"

# Time periods and date ranges
# These constants define standard time periods for analysis
class TimePeriods:
    """Standard time periods for data analysis and reporting."""
    
    # Standard periods (in days)
    LAST_7_DAYS = 7
    LAST_30_DAYS = 30
    LAST_90_DAYS = 90
    LAST_365_DAYS = 365
    
    # Business periods
    QUARTERLY = 90                       # One quarter
    YEARLY = 365                        # One year
    
    # Analysis windows
    CHURN_ANALYSIS_WINDOW = 30          # Window for churn analysis
    ENGAGEMENT_ANALYSIS_WINDOW = 90     # Window for engagement analysis
    REVENUE_ANALYSIS_WINDOW = 365       # Window for revenue analysis

# Feature flags and toggles
# These constants control feature availability and behavior
class FeatureFlags:
    """Feature flags for controlling A.U.R.A platform features."""
    
    # AI Model features
    ENABLE_PROPhet_FORECASTING = True    # Enable Prophet forecasting model
    ENABLE_CHATBOT = True                # Enable AI chatbot
    ENABLE_DECISION_ENGINE = True        # Enable rule-based decision engine
    
    # Dashboard features
    ENABLE_REAL_TIME_UPDATES = True     # Enable real-time dashboard updates
    ENABLE_EXPORT_FUNCTIONALITY = True  # Enable data export functionality
    ENABLE_ADVANCED_FILTERS = True      # Enable advanced filtering options
    
    # Data pipeline features
    ENABLE_AUTOMATIC_PROCESSING = True  # Enable automatic data processing
    ENABLE_DATA_VALIDATION = True       # Enable data validation
    ENABLE_QUALITY_MONITORING = True   # Enable data quality monitoring

# Default values for new records
# These constants provide default values for new data records
class DefaultValues:
    """Default values for new records and configurations."""
    
    # Client defaults
    DEFAULT_CLIENT_STATUS = "Active"
    DEFAULT_CLIENT_TIER = "SMB"
    DEFAULT_CLIENT_SEGMENT = "Medium-Value"
    
    # Health score defaults
    DEFAULT_HEALTH_SCORE = 50           # Neutral health score
    DEFAULT_CHURN_RISK = "Low"         # Default churn risk level
    DEFAULT_ENGAGEMENT_SCORE = 0.5     # Neutral engagement score
    
    # Model defaults
    DEFAULT_FORECAST_DAYS = 30         # Default forecast period
    DEFAULT_CONFIDENCE_LEVEL = 0.95     # Default confidence level
    DEFAULT_PREDICTION_THRESHOLD = 0.5  # Default prediction threshold

