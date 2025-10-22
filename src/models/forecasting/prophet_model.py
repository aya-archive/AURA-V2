# A.U.R.A (AI-Unified Retention Analytics) - Prophet Forecasting Model
# This module implements the Prophet forecasting model for time series prediction
# in the A.U.R.A platform, providing insights for retention strategy planning

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
import joblib
from pathlib import Path
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.graph_objects as go
from src.config.settings import settings
from src.config.constants import AIModelParams, TimePeriods

# Configure logging for Prophet model
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProphetForecastingModel:
    """
    Prophet forecasting model for A.U.R.A platform.
    
    This class implements Facebook's Prophet forecasting model for time series
    prediction in the A.U.R.A platform. It provides accurate forecasts for
    customer engagement, revenue trends, and churn patterns to support
    retention strategy planning and decision making.
    """
    
    def __init__(self):
        """Initialize the Prophet forecasting model."""
        self.model = None
        self.forecast_days = settings.prophet_forecast_days
        self.model_path = settings.forecasting_model_path
        self.trained_model_path = self.model_path / "trained_prophet_model.joblib"
        
        # Ensure model directory exists
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Prophet forecasting model initialized. Forecast days: {self.forecast_days}")
    
    def prepare_time_series_data(self, data: pd.DataFrame, 
                                date_column: str, 
                                value_column: str,
                                customer_id: Optional[str] = None) -> pd.DataFrame:
        """
        Prepare time series data for Prophet forecasting.
        
        This method transforms raw data into the format required by Prophet,
        including proper date formatting and data validation. It handles
        both individual customer time series and aggregate business metrics.
        
        Args:
            data: Raw time series data
            date_column: Name of the date column
            value_column: Name of the value column to forecast
            customer_id: Optional customer ID for individual forecasts
            
        Returns:
            pd.DataFrame: Prophet-formatted time series data
        """
        logger.info(f"Preparing time series data for forecasting")
        
        # Create a copy of the data
        ts_data = data.copy()
        
        # Convert date column to datetime
        ts_data[date_column] = pd.to_datetime(ts_data[date_column], errors='coerce')
        
        # Filter out invalid dates
        ts_data = ts_data.dropna(subset=[date_column])
        
        # If customer_id is provided, filter for that customer
        if customer_id:
            ts_data = ts_data[ts_data['customer_id'] == customer_id]
        
        # Aggregate by date if multiple records per date
        if customer_id:
            # For individual customers, sum values by date
            ts_data = ts_data.groupby(date_column)[value_column].sum().reset_index()
        else:
            # For aggregate data, ensure one record per date
            ts_data = ts_data.groupby(date_column)[value_column].sum().reset_index()
        
        # Rename columns for Prophet format
        ts_data = ts_data.rename(columns={
            date_column: 'ds',  # Prophet requires 'ds' for dates
            value_column: 'y'   # Prophet requires 'y' for values
        })
        
        # Sort by date
        ts_data = ts_data.sort_values('ds').reset_index(drop=True)
        
        # Remove any zero or negative values (Prophet works better with positive values)
        ts_data = ts_data[ts_data['y'] > 0]
        
        # Add trend and seasonality indicators
        ts_data['trend'] = np.arange(len(ts_data))
        ts_data['day_of_week'] = ts_data['ds'].dt.dayofweek
        ts_data['month'] = ts_data['ds'].dt.month
        
        logger.info(f"Time series data prepared. Records: {len(ts_data)}")
        return ts_data
    
    def train_model(self, ts_data: pd.DataFrame, 
                   custom_seasonalities: Optional[Dict[str, Any]] = None) -> None:
        """
        Train the Prophet forecasting model.
        
        This method trains the Prophet model on historical time series data,
        configuring seasonality, trend, and holiday effects. The trained model
        is saved for future use in forecasting and analysis.
        
        Args:
            ts_data: Time series data in Prophet format
            custom_seasonalities: Optional custom seasonality configurations
        """
        logger.info("Training Prophet forecasting model")
        
        # Initialize Prophet model with configuration
        self.model = Prophet(
            daily_seasonality=AIModelParams.PROPHET_DAILY_SEASONALITY,
            weekly_seasonality=AIModelParams.PROPHET_WEEKLY_SEASONALITY,
            yearly_seasonality=AIModelParams.PROPHET_YEARLY_SEASONALITY,
            changepoint_prior_scale=AIModelParams.PROPHET_CHANGEPOINT_PRIOR_SCALE,
            seasonality_mode='multiplicative',  # Better for business metrics
            interval_width=0.95,  # 95% confidence intervals
            uncertainty_samples=1000
        )
        
        # Add custom seasonalities if provided
        if custom_seasonalities:
            for seasonality_name, seasonality_config in custom_seasonalities.items():
                self.model.add_seasonality(
                    name=seasonality_name,
                    period=seasonality_config['period'],
                    fourier_order=seasonality_config.get('fourier_order', 10)
                )
        
        # Add business-specific seasonalities
        # Monthly seasonality for business cycles
        self.model.add_seasonality(
            name='monthly',
            period=30.5,
            fourier_order=5
        )
        
        # Quarterly seasonality for business quarters
        self.model.add_seasonality(
            name='quarterly',
            period=91.25,
            fourier_order=3
        )
        
        # Train the model
        try:
            self.model.fit(ts_data)
            logger.info("Prophet model training completed successfully")
            
            # Save the trained model
            self._save_model()
            
        except Exception as e:
            logger.error(f"Prophet model training failed: {str(e)}")
            raise
    
    def generate_forecast(self, periods: Optional[int] = None) -> pd.DataFrame:
        """
        Generate forecasts using the trained Prophet model.
        
        This method generates future forecasts based on the trained Prophet model,
        providing predictions for the specified number of periods ahead. The
        forecasts include confidence intervals and trend analysis.
        
        Args:
            periods: Number of periods to forecast (defaults to model configuration)
            
        Returns:
            pd.DataFrame: Forecast results with confidence intervals
        """
        if self.model is None:
            raise ValueError("Model must be trained before generating forecasts")
        
        if periods is None:
            periods = self.forecast_days
        
        logger.info(f"Generating forecast for {periods} periods")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=periods, freq='D')
        
        # Generate forecast
        forecast = self.model.predict(future)
        
        # Add forecast metadata
        forecast['forecast_generated_at'] = datetime.now()
        forecast['forecast_periods'] = periods
        forecast['model_version'] = '1.0'
        
        logger.info(f"Forecast generated successfully. Records: {len(forecast)}")
        return forecast
    
    def analyze_forecast_components(self, forecast: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze forecast components for insights.
        
        This method analyzes the forecast components including trend, seasonality,
        and residuals to provide insights into the underlying patterns and
        forecast reliability.
        
        Args:
            forecast: Prophet forecast results
            
        Returns:
            Dict[str, Any]: Component analysis results
        """
        logger.info("Analyzing forecast components")
        
        # Calculate trend strength
        trend_values = forecast['trend'].values
        trend_strength = np.std(np.diff(trend_values)) / np.mean(trend_values)
        
        # Calculate seasonality strength
        seasonal_components = ['yearly', 'monthly', 'quarterly', 'weekly', 'daily']
        seasonality_strength = {}
        
        for component in seasonal_components:
            if component in forecast.columns:
                component_values = forecast[component].values
                seasonality_strength[component] = np.std(component_values) / np.mean(forecast['yhat'].values)
        
        # Calculate forecast confidence
        confidence_interval = forecast['yhat_upper'] - forecast['yhat_lower']
        avg_confidence = np.mean(confidence_interval) / np.mean(forecast['yhat'])
        
        # Identify key insights
        insights = []
        
        if trend_strength > 0.1:
            insights.append("Strong trend detected - consider trend-based strategies")
        
        if any(strength > 0.05 for strength in seasonality_strength.values()):
            insights.append("Seasonal patterns detected - plan for seasonal variations")
        
        if avg_confidence > 0.3:
            insights.append("High forecast uncertainty - consider multiple scenarios")
        
        analysis = {
            'trend_strength': round(trend_strength, 3),
            'seasonality_strength': seasonality_strength,
            'forecast_confidence': round(avg_confidence, 3),
            'insights': insights,
            'forecast_periods': len(forecast),
            'analysis_date': datetime.now()
        }
        
        logger.info("Forecast component analysis completed")
        return analysis
    
    def create_forecast_visualization(self, forecast: pd.DataFrame, 
                                    historical_data: pd.DataFrame) -> go.Figure:
        """
        Create interactive forecast visualization.
        
        This method creates an interactive Plotly visualization of the forecast
        results, including historical data, predictions, and confidence intervals.
        The visualization helps users understand forecast trends and reliability.
        
        Args:
            forecast: Prophet forecast results
            historical_data: Historical time series data
            
        Returns:
            go.Figure: Interactive Plotly figure
        """
        logger.info("Creating forecast visualization")
        
        # Create the plot
        fig = go.Figure()
        
        # Add historical data
        fig.add_trace(go.Scatter(
            x=historical_data['ds'],
            y=historical_data['y'],
            mode='lines',
            name='Historical Data',
            line=dict(color='#004D7A', width=2)
        ))
        
        # Add forecast
        fig.add_trace(go.Scatter(
            x=forecast['ds'],
            y=forecast['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='#00B3B3', width=2)
        ))
        
        # Add confidence interval
        fig.add_trace(go.Scatter(
            x=forecast['ds'],
            y=forecast['yhat_upper'],
            mode='lines',
            name='Upper Bound',
            line=dict(color='rgba(0, 179, 179, 0.3)', width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast['ds'],
            y=forecast['yhat_lower'],
            mode='lines',
            name='Confidence Interval',
            fill='tonexty',
            fillcolor='rgba(0, 179, 179, 0.3)',
            line=dict(color='rgba(0, 179, 179, 0.3)', width=0)
        ))
        
        # Update layout
        fig.update_layout(
            title='A.U.R.A Forecast Analysis',
            xaxis_title='Date',
            yaxis_title='Value',
            hovermode='x unified',
            template='plotly_white',
            showlegend=True
        )
        
        logger.info("Forecast visualization created")
        return fig
    
    def get_forecast_insights(self, forecast: pd.DataFrame) -> Dict[str, Any]:
        """
        Extract actionable insights from forecast results.
        
        This method analyzes the forecast results to extract actionable insights
        for retention strategy planning. It identifies trends, opportunities,
        and risks that can inform business decisions.
        
        Args:
            forecast: Prophet forecast results
            
        Returns:
            Dict[str, Any]: Forecast insights and recommendations
        """
        logger.info("Extracting forecast insights")
        
        # Calculate forecast metrics
        recent_forecast = forecast.tail(30)  # Last 30 days of forecast
        forecast_trend = recent_forecast['yhat'].iloc[-1] - recent_forecast['yhat'].iloc[0]
        forecast_growth_rate = (forecast_trend / recent_forecast['yhat'].iloc[0]) * 100
        
        # Identify key patterns
        insights = {
            'forecast_summary': {
                'total_periods': len(forecast),
                'forecast_start': forecast['ds'].iloc[0].strftime('%Y-%m-%d'),
                'forecast_end': forecast['ds'].iloc[-1].strftime('%Y-%m-%d'),
                'current_value': forecast['yhat'].iloc[0],
                'forecasted_value': forecast['yhat'].iloc[-1],
                'growth_rate': round(forecast_growth_rate, 2)
            },
            'trend_analysis': {
                'trend_direction': 'increasing' if forecast_trend > 0 else 'decreasing',
                'trend_strength': abs(forecast_growth_rate),
                'trend_confidence': 'high' if abs(forecast_growth_rate) > 5 else 'medium'
            },
            'recommendations': []
        }
        
        # Generate recommendations based on forecast
        if forecast_growth_rate > 10:
            insights['recommendations'].append("Strong growth forecast - consider scaling resources")
        elif forecast_growth_rate < -10:
            insights['recommendations'].append("Declining forecast - implement retention strategies")
        elif abs(forecast_growth_rate) < 5:
            insights['recommendations'].append("Stable forecast - focus on optimization")
        
        # Add seasonal recommendations
        if 'yearly' in forecast.columns:
            yearly_seasonality = forecast['yearly'].std()
            if yearly_seasonality > 0.1:
                insights['recommendations'].append("Strong seasonal patterns - plan for seasonal variations")
        
        logger.info("Forecast insights extracted")
        return insights
    
    def _save_model(self) -> None:
        """Save the trained Prophet model."""
        try:
            joblib.dump(self.model, self.trained_model_path)
            logger.info(f"Prophet model saved to {self.trained_model_path}")
        except Exception as e:
            logger.error(f"Failed to save Prophet model: {str(e)}")
            raise
    
    def load_model(self) -> bool:
        """
        Load a previously trained Prophet model.
        
        This method loads a previously trained Prophet model from disk,
        allowing for quick forecasting without retraining.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            if self.trained_model_path.exists():
                self.model = joblib.load(self.trained_model_path)
                logger.info(f"Prophet model loaded from {self.trained_model_path}")
                return True
            else:
                logger.warning("No trained model found")
                return False
        except Exception as e:
            logger.error(f"Failed to load Prophet model: {str(e)}")
            return False
    
    def forecast_customer_engagement(self, customer_data: pd.DataFrame, 
                                   customer_id: str) -> Dict[str, Any]:
        """
        Forecast engagement for a specific customer.
        
        This method creates a personalized engagement forecast for a specific
        customer, helping identify engagement trends and potential churn risks.
        
        Args:
            customer_data: Customer engagement data
            customer_id: Customer ID to forecast
            
        Returns:
            Dict[str, Any]: Customer engagement forecast results
        """
        logger.info(f"Forecasting engagement for customer {customer_id}")
        
        # Prepare customer-specific time series
        ts_data = self.prepare_time_series_data(
            customer_data, 
            'event_timestamp', 
            'engagement_score',
            customer_id
        )
        
        if len(ts_data) < 7:  # Need at least a week of data
            return {
                'error': 'Insufficient data for forecasting',
                'customer_id': customer_id,
                'data_points': len(ts_data)
            }
        
        # Train model for this customer
        self.train_model(ts_data)
        
        # Generate forecast
        forecast = self.generate_forecast()
        
        # Analyze components
        analysis = self.analyze_forecast_components(forecast)
        
        # Extract insights
        insights = self.get_forecast_insights(forecast)
        
        return {
            'customer_id': customer_id,
            'forecast': forecast,
            'analysis': analysis,
            'insights': insights,
            'forecast_generated_at': datetime.now()
        }
    
    def forecast_business_metrics(self, business_data: pd.DataFrame, 
                                metric_column: str) -> Dict[str, Any]:
        """
        Forecast business-level metrics.
        
        This method creates forecasts for business-level metrics such as
        total revenue, customer count, or engagement levels to support
        strategic planning and resource allocation.
        
        Args:
            business_data: Business metrics data
            metric_column: Column name for the metric to forecast
            
        Returns:
            Dict[str, Any]: Business metrics forecast results
        """
        logger.info(f"Forecasting business metrics: {metric_column}")
        
        # Prepare business time series
        ts_data = self.prepare_time_series_data(
            business_data,
            'date',
            metric_column
        )
        
        if len(ts_data) < 30:  # Need at least a month of data
            return {
                'error': 'Insufficient data for business forecasting',
                'metric': metric_column,
                'data_points': len(ts_data)
            }
        
        # Train model
        self.train_model(ts_data)
        
        # Generate forecast
        forecast = self.generate_forecast()
        
        # Analyze components
        analysis = self.analyze_forecast_components(forecast)
        
        # Extract insights
        insights = self.get_forecast_insights(forecast)
        
        return {
            'metric': metric_column,
            'forecast': forecast,
            'analysis': analysis,
            'insights': insights,
            'forecast_generated_at': datetime.now()
        }

def main():
    """Main function to demonstrate Prophet forecasting functionality."""
    logger.info("Starting A.U.R.A Prophet forecasting demonstration")
    
    # Initialize Prophet model
    prophet_model = ProphetForecastingModel()
    
    # Create sample time series data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    values = np.random.normal(100, 10, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 20
    
    sample_data = pd.DataFrame({
        'ds': dates,
        'y': values
    })
    
    # Train model
    prophet_model.train_model(sample_data)
    
    # Generate forecast
    forecast = prophet_model.generate_forecast(periods=30)
    
    # Analyze components
    analysis = prophet_model.analyze_forecast_components(forecast)
    
    # Extract insights
    insights = prophet_model.get_forecast_insights(forecast)
    
    # Print results
    print("\n" + "="*50)
    print("A.U.R.A Prophet Forecasting Results")
    print("="*50)
    print(f"Forecast periods: {len(forecast)}")
    print(f"Trend strength: {analysis['trend_strength']}")
    print(f"Forecast confidence: {analysis['forecast_confidence']}")
    print(f"Growth rate: {insights['forecast_summary']['growth_rate']}%")
    print(f"Recommendations: {len(insights['recommendations'])}")
    
    logger.info("A.U.R.A Prophet forecasting demonstration completed")

if __name__ == "__main__":
    main()

