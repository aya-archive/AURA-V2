# A.U.R.A (Adaptive User Retention Assistant) - Application Settings
# This module contains all configuration settings for the A.U.R.A platform
# including environment variables, data paths, model parameters, and API keys

import os
from pathlib import Path
from typing import Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Application settings for A.U.R.A platform.
    
    This class manages all configuration parameters including data paths,
    model settings, and environment-specific configurations. It uses Pydantic
    for validation and type safety, ensuring all settings are properly configured.
    """
    
    # Application metadata
    app_name: str = "A.U.R.A"
    app_version: str = "1.0.0"
    PROJECT_VERSION: str = "1.0.0"  # Alias for compatibility
    app_description: str = "AI-Unified Retention Analytics Platform"
    
    # Environment configuration
    environment: str = Field(default="development", description="Environment: development, staging, production")
    debug: bool = Field(default=True, description="Enable debug mode for development")
    
    # Data paths - Medallion architecture directories
    # These paths define where data is stored at each layer of the Medallion architecture
    data_root: Path = Path("data")
    bronze_path: Path = data_root / "bronze"  # Raw data landing zone
    silver_path: Path = data_root / "silver"   # Cleaned and enriched data
    gold_path: Path = data_root / "gold"       # Business-ready aggregated data
    temp_path: Path = data_root / "temp"       # Temporary processing files
    
    # Model storage paths
    # These paths store trained AI models for forecasting, decision making, and chatbot
    models_root: Path = Path("models")
    forecasting_model_path: Path = models_root / "forecasting"
    decision_engine_path: Path = models_root / "decision_engine"
    chatbot_model_path: Path = models_root / "chatbot"
    
    # Application storage paths
    uploads_path: Path = Path("uploads")      # User uploaded files
    logs_path: Path = Path("logs")            # Application logs
    
    # Database configuration (for future use)
    database_url: str = Field(default="sqlite:///aura.db", description="Database connection URL")
    
    # AI Model parameters
    # These parameters control the behavior of AI models and decision engines
    prophet_forecast_days: int = Field(default=30, description="Number of days to forecast ahead")
    churn_risk_threshold_high: float = Field(default=0.7, description="High churn risk threshold")
    churn_risk_threshold_medium: float = Field(default=0.4, description="Medium churn risk threshold")
    health_score_weights: Dict[str, float] = Field(
        default={
            "engagement": 0.4,    # 40% weight for engagement metrics
            "revenue": 0.3,       # 30% weight for revenue metrics  
            "support": 0.2,       # 20% weight for support interactions
            "nps": 0.1           # 10% weight for NPS scores
        },
        description="Weights for calculating client health scores"
    )
    
    # Chatbot configuration
    # Parameters for the AI chatbot's NLP and conversational capabilities
    chatbot_max_context_length: int = Field(default=4000, description="Maximum context length for chatbot")
    chatbot_temperature: float = Field(default=0.7, description="Temperature for chatbot response generation")
    chatbot_max_tokens: int = Field(default=500, description="Maximum tokens for chatbot responses")
    
    # Streamlit configuration
    # Settings for the Streamlit dashboard and user interface
    streamlit_page_title: str = "A.U.R.A - AI Retention Analytics"
    streamlit_page_icon: str = "🤖"
    streamlit_layout: str = "wide"
    streamlit_initial_sidebar_state: str = "expanded"
    
    # API configuration (for future microservices)
    api_host: str = Field(default="0.0.0.0", description="API host address")
    api_port: int = Field(default=8000, description="API port number")
    api_workers: int = Field(default=1, description="Number of API workers")
    
    # Security settings
    # Configuration for authentication and data security
    secret_key: str = Field(default="aura-secret-key-change-in-production", description="Secret key for encryption")
    jwt_secret: str = Field(default="aura-jwt-secret", description="JWT secret for token generation")
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_expiration_hours: int = Field(default=24, description="JWT token expiration in hours")
    
    # Monitoring and logging
    # Configuration for application monitoring and observability
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format")
    enable_metrics: bool = Field(default=True, description="Enable Prometheus metrics collection")
    
    # Performance settings
    # Configuration for optimizing application performance
    cache_ttl: int = Field(default=3600, description="Cache time-to-live in seconds")
    max_workers: int = Field(default=4, description="Maximum number of worker processes")
    batch_size: int = Field(default=1000, description="Batch size for data processing")
    
    # External service configuration (for future integrations)
    # These settings will be used when integrating with external services
    openai_api_key: str = Field(default="", description="OpenAI API key for advanced NLP")
    aws_access_key: str = Field(default="", description="AWS access key for cloud services")
    aws_secret_key: str = Field(default="", description="AWS secret key for cloud services")
    aws_region: str = Field(default="us-east-1", description="AWS region for cloud services")
    
    class Config:
        """Pydantic configuration for settings validation."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    def get_data_path(self, layer: str) -> Path:
        """
        Get the data path for a specific Medallion layer.
        
        Args:
            layer: The Medallion layer ('bronze', 'silver', 'gold', 'temp')
            
        Returns:
            Path: The full path to the specified data layer
            
        Raises:
            ValueError: If layer is not one of the supported Medallion layers
        """
        layer_paths = {
            'bronze': self.bronze_path,
            'silver': self.silver_path, 
            'gold': self.gold_path,
            'temp': self.temp_path
        }
        
        if layer not in layer_paths:
            raise ValueError(f"Invalid layer: {layer}. Must be one of {list(layer_paths.keys())}")
            
        return layer_paths[layer]
    
    def get_model_path(self, model_type: str) -> Path:
        """
        Get the model path for a specific AI model type.
        
        Args:
            model_type: The type of model ('forecasting', 'decision_engine', 'chatbot')
            
        Returns:
            Path: The full path to the specified model directory
            
        Raises:
            ValueError: If model_type is not supported
        """
        model_paths = {
            'forecasting': self.forecasting_model_path,
            'decision_engine': self.decision_engine_path,
            'chatbot': self.chatbot_model_path
        }
        
        if model_type not in model_paths:
            raise ValueError(f"Invalid model_type: {model_type}. Must be one of {list(model_paths.keys())}")
            
        return model_paths[model_type]
    
    def ensure_directories(self) -> None:
        """
        Ensure all required directories exist.
        
        This method creates all necessary directories for the A.U.R.A platform
        if they don't already exist, ensuring the application can run properly.
        """
        directories = [
            self.data_root,
            self.bronze_path,
            self.silver_path, 
            self.gold_path,
            self.temp_path,
            self.models_root,
            self.forecasting_model_path,
            self.decision_engine_path,
            self.chatbot_model_path,
            self.uploads_path,
            self.logs_path
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

# Global settings instance
# This instance is used throughout the application for configuration
settings = Settings()

# Ensure all directories exist when settings are loaded
settings.ensure_directories()
