# A.U.R.A (AI-Unified Retention Analytics) - Data Ingestion Module
# This module handles the ingestion of raw data into the Bronze layer
# of the Medallion architecture, including validation and basic preprocessing

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
from src.config.settings import settings
from src.config.constants import ValidationRules

# Configure logging for data ingestion
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataIngestion:
    """
    Handles data ingestion from various sources into the Bronze layer.
    
    This class manages the loading, validation, and initial processing of raw data
    from different sources (CSV files, APIs, databases) into the Bronze layer
    of the Medallion architecture. It ensures data quality and consistency
    while preserving the original data fidelity for traceability.
    """
    
    def __init__(self):
        """Initialize the data ingestion module with configuration."""
        self.bronze_path = settings.bronze_path
        self.ingestion_timestamp = datetime.now()
        
        # Ensure Bronze layer directory exists
        self.bronze_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Data ingestion initialized. Bronze path: {self.bronze_path}")
    
    def load_csv_file(self, file_path: Path, **kwargs) -> pd.DataFrame:
        """
        Load a CSV file with error handling and basic validation.
        
        This method loads CSV files from the Bronze layer with proper error handling,
        data type inference, and basic validation to ensure data quality.
        
        Args:
            file_path: Path to the CSV file to load
            **kwargs: Additional arguments to pass to pd.read_csv
            
        Returns:
            pd.DataFrame: Loaded data with proper data types
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            pd.errors.EmptyDataError: If the file is empty
            ValueError: If data validation fails
        """
        try:
            logger.info(f"Loading CSV file: {file_path}")
            
            # Load CSV with error handling
            df = pd.read_csv(file_path, **kwargs)
            
            if df.empty:
                logger.warning(f"Empty file loaded: {file_path}")
                return df
            
            # Basic validation
            self._validate_dataframe(df, file_path.name)
            
            logger.info(f"Successfully loaded {len(df)} records from {file_path}")
            return df
            
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except pd.errors.EmptyDataError:
            logger.error(f"Empty file: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading {file_path}: {str(e)}")
            raise
    
    def _validate_dataframe(self, df: pd.DataFrame, file_name: str) -> None:
        """
        Validate DataFrame for basic data quality issues.
        
        This method performs basic validation on the loaded DataFrame to ensure
        data quality and consistency. It checks for required columns, data types,
        and common data quality issues.
        
        Args:
            df: DataFrame to validate
            file_name: Name of the file for error reporting
            
        Raises:
            ValueError: If validation fails
        """
        logger.debug(f"Validating DataFrame from {file_name}")
        
        # Check for empty DataFrame
        if df.empty:
            raise ValueError(f"Empty DataFrame from {file_name}")
        
        # Check for required columns based on file type
        required_columns = self._get_required_columns(file_name)
        missing_columns = set(required_columns) - set(df.columns)
        
        if missing_columns:
            raise ValueError(f"Missing required columns in {file_name}: {missing_columns}")
        
        # Check for completely null columns
        null_columns = df.columns[df.isnull().all()].tolist()
        if null_columns:
            logger.warning(f"Columns with all null values in {file_name}: {null_columns}")
        
        # Check for duplicate rows
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            logger.warning(f"Found {duplicate_count} duplicate rows in {file_name}")
        
        logger.debug(f"DataFrame validation completed for {file_name}")
    
    def _get_required_columns(self, file_name: str) -> List[str]:
        """
        Get required columns for a specific file type.
        
        This method defines the required columns for each Bronze layer file type
        based on the A.U.R.A data schema. It ensures data consistency and
        completeness across different data sources.
        
        Args:
            file_name: Name of the file to get required columns for
            
        Returns:
            List[str]: List of required column names
        """
        if "customer" in file_name.lower():
            return ["customer_id", "first_name", "last_name", "email", "account_creation_date", "status"]
        elif "transaction" in file_name.lower():
            return ["transaction_id", "customer_id", "transaction_date", "amount", "currency"]
        elif "engagement" in file_name.lower():
            return ["event_id", "customer_id", "event_type", "event_timestamp"]
        elif "support" in file_name.lower():
            return ["ticket_id", "customer_id", "interaction_type", "created_at", "status"]
        elif "survey" in file_name.lower():
            return ["survey_response_id", "customer_id", "response_date", "nps_score"]
        else:
            return []
    
    def add_ingestion_metadata(self, df: pd.DataFrame, source_system: str = "CSV_File") -> pd.DataFrame:
        """
        Add ingestion metadata to DataFrame.
        
        This method adds metadata columns to track data lineage and ingestion
        information. This is crucial for the Medallion architecture as it
        preserves the original data source and ingestion timestamp.
        
        Args:
            df: DataFrame to add metadata to
            source_system: Source system identifier
            
        Returns:
            pd.DataFrame: DataFrame with added metadata columns
        """
        logger.debug(f"Adding ingestion metadata for {len(df)} records")
        
        # Add ingestion timestamp if not present
        if 'ingestion_timestamp' not in df.columns:
            df['ingestion_timestamp'] = self.ingestion_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        # Add source system if not present
        if 'source_system' not in df.columns:
            df['source_system'] = source_system
        
        # Add data quality flags
        df['data_quality_score'] = self._calculate_data_quality_score(df)
        
        logger.debug("Ingestion metadata added successfully")
        return df
    
    def _calculate_data_quality_score(self, df: pd.DataFrame) -> float:
        """
        Calculate a data quality score for the DataFrame.
        
        This method calculates a simple data quality score based on completeness,
        consistency, and other quality metrics. The score helps identify data
        quality issues early in the pipeline.
        
        Args:
            df: DataFrame to calculate quality score for
            
        Returns:
            float: Data quality score between 0 and 1
        """
        if df.empty:
            return 0.0
        
        # Calculate completeness score (percentage of non-null values)
        completeness = 1 - (df.isnull().sum().sum() / (len(df) * len(df.columns)))
        
        # Calculate consistency score (based on data type consistency)
        consistency = 1.0  # Simplified for now
        
        # Calculate uniqueness score (based on duplicate percentage)
        uniqueness = 1 - (df.duplicated().sum() / len(df))
        
        # Weighted average of quality metrics
        quality_score = (completeness * 0.5 + consistency * 0.3 + uniqueness * 0.2)
        
        return round(quality_score, 3)
    
    def load_bronze_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all Bronze layer data files.
        
        This method loads all available Bronze layer data files and returns
        them as a dictionary. It handles missing files gracefully and provides
        comprehensive logging for data ingestion monitoring.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of loaded DataFrames
        """
        logger.info("Loading all Bronze layer data files")
        
        bronze_data = {}
        
        # Define Bronze layer files to load
        bronze_files = {
            'customers': 'raw_customer_demographics.csv',
            'transactions': 'raw_transactions.csv',
            'engagement': 'raw_engagement_logs.csv',
            'support': 'raw_support_interactions.csv',
            'surveys': 'raw_feedback_surveys.csv'
        }
        
        for data_type, file_name in bronze_files.items():
            file_path = self.bronze_path / file_name
            
            try:
                if file_path.exists():
                    df = self.load_csv_file(file_path)
                    df = self.add_ingestion_metadata(df, f"Bronze_{data_type}")
                    bronze_data[data_type] = df
                    logger.info(f"Loaded {data_type} data: {len(df)} records")
                else:
                    logger.warning(f"Bronze file not found: {file_path}")
                    bronze_data[data_type] = pd.DataFrame()
                    
            except Exception as e:
                logger.error(f"Error loading {data_type} data: {str(e)}")
                bronze_data[data_type] = pd.DataFrame()
        
        logger.info(f"Bronze data loading completed. Loaded {len(bronze_data)} data types")
        return bronze_data
    
    def validate_bronze_data(self, bronze_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Validate Bronze layer data for quality and consistency.
        
        This method performs comprehensive validation of Bronze layer data
        to ensure data quality and consistency before processing. It checks
        for data completeness, consistency, and business rule compliance.
        
        Args:
            bronze_data: Dictionary of Bronze layer DataFrames
            
        Returns:
            Dict[str, Any]: Validation results and statistics
        """
        logger.info("Validating Bronze layer data")
        
        validation_results = {
            'total_records': 0,
            'data_quality_scores': {},
            'validation_errors': [],
            'warnings': []
        }
        
        for data_type, df in bronze_data.items():
            if df.empty:
                validation_results['warnings'].append(f"No data found for {data_type}")
                continue
            
            # Calculate data quality score
            quality_score = self._calculate_data_quality_score(df)
            validation_results['data_quality_scores'][data_type] = quality_score
            
            # Add to total records
            validation_results['total_records'] += len(df)
            
            # Check for critical data quality issues
            if quality_score < 0.7:
                validation_results['validation_errors'].append(
                    f"Low data quality score for {data_type}: {quality_score}"
                )
            
            # Check for missing critical data
            if data_type == 'customers' and 'customer_id' in df.columns:
                missing_customer_ids = df['customer_id'].isnull().sum()
                if missing_customer_ids > 0:
                    validation_results['validation_errors'].append(
                        f"Missing customer IDs in {data_type}: {missing_customer_ids}"
                    )
        
        logger.info(f"Bronze data validation completed. Total records: {validation_results['total_records']}")
        return validation_results
    
    def get_data_summary(self, bronze_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Generate summary statistics for Bronze layer data.
        
        This method generates comprehensive summary statistics for all Bronze
        layer data, including record counts, data quality metrics, and
        basic descriptive statistics for monitoring and reporting.
        
        Args:
            bronze_data: Dictionary of Bronze layer DataFrames
            
        Returns:
            Dict[str, Any]: Summary statistics and metrics
        """
        logger.info("Generating Bronze layer data summary")
        
        summary = {
            'data_types': list(bronze_data.keys()),
            'record_counts': {},
            'date_ranges': {},
            'data_quality': {},
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        for data_type, df in bronze_data.items():
            if df.empty:
                summary['record_counts'][data_type] = 0
                continue
            
            # Record count
            summary['record_counts'][data_type] = len(df)
            
            # Date range analysis
            date_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
            if not date_columns:
                # Try to find date-like columns
                date_columns = [col for col in df.columns if 'date' in col.lower() or 'timestamp' in col.lower()]
            
            if date_columns:
                try:
                    date_col = date_columns[0]
                    if df[date_col].dtype == 'object':
                        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                    
                    summary['date_ranges'][data_type] = {
                        'earliest': df[date_col].min().strftime('%Y-%m-%d') if not df[date_col].isnull().all() else None,
                        'latest': df[date_col].max().strftime('%Y-%m-%d') if not df[date_col].isnull().all() else None
                    }
                except Exception as e:
                    logger.warning(f"Could not analyze date range for {data_type}: {str(e)}")
            
            # Data quality metrics
            summary['data_quality'][data_type] = {
                'completeness': 1 - (df.isnull().sum().sum() / (len(df) * len(df.columns))),
                'uniqueness': 1 - (df.duplicated().sum() / len(df)),
                'columns': len(df.columns),
                'rows': len(df)
            }
        
        logger.info("Bronze layer data summary generated")
        return summary

def main():
    """Main function to demonstrate data ingestion functionality."""
    logger.info("Starting A.U.R.A data ingestion process")
    
    # Initialize data ingestion
    ingestion = DataIngestion()
    
    # Load Bronze layer data
    bronze_data = ingestion.load_bronze_data()
    
    # Validate data
    validation_results = ingestion.validate_bronze_data(bronze_data)
    
    # Generate summary
    summary = ingestion.get_data_summary(bronze_data)
    
    # Print results
    print("\n" + "="*50)
    print("A.U.R.A Data Ingestion Results")
    print("="*50)
    print(f"Total records loaded: {validation_results['total_records']}")
    print(f"Data types: {', '.join(summary['data_types'])}")
    print("\nRecord counts:")
    for data_type, count in summary['record_counts'].items():
        print(f"  {data_type}: {count:,}")
    
    print("\nData quality scores:")
    for data_type, score in validation_results['data_quality_scores'].items():
        print(f"  {data_type}: {score:.3f}")
    
    if validation_results['validation_errors']:
        print("\nValidation errors:")
        for error in validation_results['validation_errors']:
            print(f"  - {error}")
    
    if validation_results['warnings']:
        print("\nWarnings:")
        for warning in validation_results['warnings']:
            print(f"  - {warning}")
    
    logger.info("A.U.R.A data ingestion process completed")

if __name__ == "__main__":
    main()

