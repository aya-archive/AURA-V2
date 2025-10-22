# A.U.R.A (AI-Unified Retention Analytics) - Data Pipeline Orchestrator
# This module orchestrates the complete data pipeline from Bronze to Gold layers
# of the Medallion architecture, ensuring data quality and consistency

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import logging
import traceback
from src.config.settings import settings
from src.data_pipeline.ingest import DataIngestion
from src.data_pipeline.silver_transform import SilverTransform
from src.data_pipeline.gold_agg import GoldAggregation

# Configure logging for pipeline orchestration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/aura_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataPipelineOrchestrator:
    """
    Orchestrates the complete A.U.R.A data pipeline.
    
    This class manages the end-to-end data pipeline from Bronze layer ingestion
    through Silver layer transformation to Gold layer aggregation. It ensures
    data quality, consistency, and provides comprehensive monitoring and logging.
    """
    
    def __init__(self):
        """Initialize the data pipeline orchestrator."""
        self.ingestion = DataIngestion()
        self.silver_transform = SilverTransform()
        self.gold_agg = GoldAggregation()
        
        # Pipeline execution tracking
        self.execution_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.pipeline_status = {
            'bronze_ingestion': False,
            'silver_transformation': False,
            'gold_aggregation': False,
            'overall_success': False
        }
        
        # Ensure logs directory exists
        Path('logs').mkdir(exist_ok=True)
        
        logger.info(f"Data pipeline orchestrator initialized. Execution ID: {self.execution_id}")
    
    def run_complete_pipeline(self) -> Dict[str, Any]:
        """
        Run the complete data pipeline from Bronze to Gold.
        
        This method orchestrates the entire data pipeline, including Bronze layer
        ingestion, Silver layer transformation, and Gold layer aggregation.
        It provides comprehensive error handling and monitoring.
        
        Returns:
            Dict[str, Any]: Pipeline execution results and statistics
        """
        logger.info("Starting complete A.U.R.A data pipeline execution")
        
        pipeline_results = {
            'execution_id': self.execution_id,
            'start_time': datetime.now(),
            'bronze_data': {},
            'silver_data': {},
            'gold_data': {},
            'errors': [],
            'warnings': [],
            'statistics': {}
        }
        
        try:
            # Step 1: Bronze Layer Ingestion
            logger.info("Step 1: Bronze Layer Ingestion")
            bronze_data = self._run_bronze_ingestion()
            pipeline_results['bronze_data'] = bronze_data
            self.pipeline_status['bronze_ingestion'] = True
            
            # Step 2: Silver Layer Transformation
            logger.info("Step 2: Silver Layer Transformation")
            silver_data = self._run_silver_transformation(bronze_data)
            pipeline_results['silver_data'] = silver_data
            self.pipeline_status['silver_transformation'] = True
            
            # Step 3: Gold Layer Aggregation
            logger.info("Step 3: Gold Layer Aggregation")
            gold_data = self._run_gold_aggregation(silver_data)
            pipeline_results['gold_data'] = gold_data
            self.pipeline_status['gold_aggregation'] = True
            
            # Step 4: Generate Pipeline Statistics
            logger.info("Step 4: Generating Pipeline Statistics")
            pipeline_results['statistics'] = self._generate_pipeline_statistics(
                bronze_data, silver_data, gold_data
            )
            
            # Mark overall success
            self.pipeline_status['overall_success'] = True
            pipeline_results['end_time'] = datetime.now()
            pipeline_results['duration'] = (
                pipeline_results['end_time'] - pipeline_results['start_time']
            ).total_seconds()
            
            logger.info("A.U.R.A data pipeline execution completed successfully")
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            pipeline_results['errors'].append(str(e))
            pipeline_results['end_time'] = datetime.now()
            pipeline_results['duration'] = (
                pipeline_results['end_time'] - pipeline_results['start_time']
            ).total_seconds()
        
        # Log final results
        self._log_pipeline_results(pipeline_results)
        
        return pipeline_results
    
    def _run_bronze_ingestion(self) -> Dict[str, pd.DataFrame]:
        """
        Execute Bronze layer data ingestion.
        
        This method handles the ingestion of raw data from various sources
        into the Bronze layer, including validation and quality checks.
        
        Returns:
            Dict[str, pd.DataFrame]: Bronze layer data
        """
        logger.info("Executing Bronze layer ingestion")
        
        try:
            # Load Bronze layer data
            bronze_data = self.ingestion.load_bronze_data()
            
            # Validate Bronze data
            validation_results = self.ingestion.validate_bronze_data(bronze_data)
            
            # Check for validation errors
            if validation_results['validation_errors']:
                for error in validation_results['validation_errors']:
                    logger.warning(f"Bronze validation warning: {error}")
            
            # Generate summary
            summary = self.ingestion.get_data_summary(bronze_data)
            
            logger.info(f"Bronze ingestion completed. Total records: {validation_results['total_records']}")
            return bronze_data
            
        except Exception as e:
            logger.error(f"Bronze ingestion failed: {str(e)}")
            raise
    
    def _run_silver_transformation(self, bronze_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Execute Silver layer data transformation.
        
        This method handles the transformation of Bronze layer data into
        Silver layer format through cleaning, standardization, and enrichment.
        
        Args:
            bronze_data: Bronze layer data
            
        Returns:
            Dict[str, pd.DataFrame]: Silver layer data
        """
        logger.info("Executing Silver layer transformation")
        
        try:
            # Transform Bronze to Silver
            silver_data = self.silver_transform.transform_bronze_to_silver(bronze_data)
            
            # Validate Silver data
            silver_validation = self._validate_silver_data(silver_data)
            
            if silver_validation['errors']:
                for error in silver_validation['errors']:
                    logger.warning(f"Silver validation warning: {error}")
            
            logger.info(f"Silver transformation completed. Data types: {len(silver_data)}")
            return silver_data
            
        except Exception as e:
            logger.error(f"Silver transformation failed: {str(e)}")
            raise
    
    def _run_gold_aggregation(self, silver_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Execute Gold layer data aggregation.
        
        This method handles the aggregation of Silver layer data into
        Gold layer business-ready datasets for dashboards and AI models.
        
        Args:
            silver_data: Silver layer data
            
        Returns:
            Dict[str, pd.DataFrame]: Gold layer data
        """
        logger.info("Executing Gold layer aggregation")
        
        try:
            # Aggregate Silver to Gold
            gold_data = self.gold_agg.aggregate_silver_to_gold(silver_data)
            
            # Validate Gold data
            gold_validation = self._validate_gold_data(gold_data)
            
            if gold_validation['errors']:
                for error in gold_validation['errors']:
                    logger.warning(f"Gold validation warning: {error}")
            
            logger.info(f"Gold aggregation completed. Data types: {len(gold_data)}")
            return gold_data
            
        except Exception as e:
            logger.error(f"Gold aggregation failed: {str(e)}")
            raise
    
    def _validate_silver_data(self, silver_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Validate Silver layer data quality.
        
        This method performs comprehensive validation of Silver layer data
        to ensure data quality and consistency for downstream processing.
        
        Args:
            silver_data: Silver layer data
            
        Returns:
            Dict[str, Any]: Validation results
        """
        validation_results = {'errors': [], 'warnings': []}
        
        for data_type, df in silver_data.items():
            if df.empty:
                validation_results['warnings'].append(f"Empty Silver data: {data_type}")
                continue
            
            # Check for required columns in customer profiles
            if data_type == 'customer_profiles':
                required_columns = ['customer_pk', 'current_health_score', 'churn_risk_level']
                missing_columns = set(required_columns) - set(df.columns)
                if missing_columns:
                    validation_results['errors'].append(f"Missing columns in {data_type}: {missing_columns}")
            
            # Check for data quality issues
            if 'current_health_score' in df.columns:
                invalid_scores = df['current_health_score'].isnull().sum()
                if invalid_scores > 0:
                    validation_results['warnings'].append(f"Invalid health scores in {data_type}: {invalid_scores}")
        
        return validation_results
    
    def _validate_gold_data(self, gold_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Validate Gold layer data quality.
        
        This method performs comprehensive validation of Gold layer data
        to ensure business-ready datasets are properly formatted and complete.
        
        Args:
            gold_data: Gold layer data
            
        Returns:
            Dict[str, Any]: Validation results
        """
        validation_results = {'errors': [], 'warnings': []}
        
        for data_type, df in gold_data.items():
            if df.empty:
                validation_results['warnings'].append(f"Empty Gold data: {data_type}")
                continue
            
            # Check for required columns in customer 360 view
            if data_type == 'customer_360_dashboard_view':
                required_columns = ['customer_pk', 'current_health_score', 'churn_risk_level', 'recommended_action']
                missing_columns = set(required_columns) - set(df.columns)
                if missing_columns:
                    validation_results['errors'].append(f"Missing columns in {data_type}: {missing_columns}")
            
            # Check for data quality issues
            if 'current_health_score' in df.columns:
                invalid_scores = df['current_health_score'].isnull().sum()
                if invalid_scores > 0:
                    validation_results['warnings'].append(f"Invalid health scores in {data_type}: {invalid_scores}")
        
        return validation_results
    
    def _generate_pipeline_statistics(self, bronze_data: Dict[str, pd.DataFrame],
                                    silver_data: Dict[str, pd.DataFrame],
                                    gold_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Generate comprehensive pipeline statistics.
        
        This method generates detailed statistics about the pipeline execution,
        including data volumes, quality metrics, and processing times.
        
        Args:
            bronze_data: Bronze layer data
            silver_data: Silver layer data
            gold_data: Gold layer data
            
        Returns:
            Dict[str, Any]: Pipeline statistics
        """
        statistics = {
            'bronze_records': sum(len(df) for df in bronze_data.values() if not df.empty),
            'silver_records': sum(len(df) for df in silver_data.values() if not df.empty),
            'gold_records': sum(len(df) for df in gold_data.values() if not df.empty),
            'data_quality_scores': {},
            'processing_summary': {}
        }
        
        # Calculate data quality scores
        for data_type, df in bronze_data.items():
            if not df.empty:
                quality_score = 1 - (df.isnull().sum().sum() / (len(df) * len(df.columns)))
                statistics['data_quality_scores'][f'bronze_{data_type}'] = round(quality_score, 3)
        
        # Calculate processing summary
        statistics['processing_summary'] = {
            'bronze_files_processed': len([df for df in bronze_data.values() if not df.empty]),
            'silver_files_processed': len([df for df in silver_data.values() if not df.empty]),
            'gold_files_processed': len([df for df in gold_data.values() if not df.empty]),
            'total_processing_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return statistics
    
    def _log_pipeline_results(self, results: Dict[str, Any]) -> None:
        """
        Log comprehensive pipeline results.
        
        This method logs detailed results of the pipeline execution,
        including statistics, errors, and warnings for monitoring and debugging.
        
        Args:
            results: Pipeline execution results
        """
        logger.info("="*60)
        logger.info("A.U.R.A DATA PIPELINE EXECUTION RESULTS")
        logger.info("="*60)
        logger.info(f"Execution ID: {results['execution_id']}")
        logger.info(f"Start Time: {results['start_time']}")
        logger.info(f"End Time: {results['end_time']}")
        logger.info(f"Duration: {results['duration']:.2f} seconds")
        logger.info(f"Overall Success: {self.pipeline_status['overall_success']}")
        
        # Log statistics
        if 'statistics' in results:
            stats = results['statistics']
            logger.info(f"Bronze Records: {stats['bronze_records']:,}")
            logger.info(f"Silver Records: {stats['silver_records']:,}")
            logger.info(f"Gold Records: {stats['gold_records']:,}")
        
        # Log errors
        if results['errors']:
            logger.error(f"Errors: {len(results['errors'])}")
            for error in results['errors']:
                logger.error(f"  - {error}")
        
        # Log warnings
        if results['warnings']:
            logger.warning(f"Warnings: {len(results['warnings'])}")
            for warning in results['warnings']:
                logger.warning(f"  - {warning}")
        
        logger.info("="*60)
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Get current pipeline execution status.
        
        This method returns the current status of the pipeline execution,
        including which steps have completed successfully and any errors.
        
        Returns:
            Dict[str, Any]: Pipeline status information
        """
        return {
            'execution_id': self.execution_id,
            'status': self.pipeline_status,
            'overall_success': self.pipeline_status['overall_success'],
            'timestamp': datetime.now()
        }
    
    def run_incremental_pipeline(self, since_date: datetime) -> Dict[str, Any]:
        """
        Run incremental pipeline for data since a specific date.
        
        This method runs an incremental pipeline that only processes data
        that has been updated since the specified date, improving efficiency
        for regular pipeline runs.
        
        Args:
            since_date: Date to process data since
            
        Returns:
            Dict[str, Any]: Incremental pipeline results
        """
        logger.info(f"Starting incremental pipeline since {since_date}")
        
        # For now, run the complete pipeline
        # In a production environment, this would filter data by date
        return self.run_complete_pipeline()
    
    def validate_pipeline_data(self) -> Dict[str, Any]:
        """
        Validate all pipeline data for quality and consistency.
        
        This method performs comprehensive validation of all data layers
        to ensure data quality and consistency across the entire pipeline.
        
        Returns:
            Dict[str, Any]: Validation results
        """
        logger.info("Validating pipeline data")
        
        validation_results = {
            'bronze_validation': {},
            'silver_validation': {},
            'gold_validation': {},
            'overall_quality_score': 0.0
        }
        
        try:
            # Validate Bronze layer
            bronze_data = self.ingestion.load_bronze_data()
            bronze_validation = self.ingestion.validate_bronze_data(bronze_data)
            validation_results['bronze_validation'] = bronze_validation
            
            # Validate Silver layer
            silver_data = self.silver_transform.transform_bronze_to_silver(bronze_data)
            silver_validation = self._validate_silver_data(silver_data)
            validation_results['silver_validation'] = silver_validation
            
            # Validate Gold layer
            gold_data = self.gold_agg.aggregate_silver_to_gold(silver_data)
            gold_validation = self._validate_gold_data(gold_data)
            validation_results['gold_validation'] = gold_validation
            
            # Calculate overall quality score
            bronze_scores = list(bronze_validation['data_quality_scores'].values())
            if bronze_scores:
                validation_results['overall_quality_score'] = sum(bronze_scores) / len(bronze_scores)
            
            logger.info(f"Pipeline validation completed. Overall quality: {validation_results['overall_quality_score']:.3f}")
            
        except Exception as e:
            logger.error(f"Pipeline validation failed: {str(e)}")
            validation_results['error'] = str(e)
        
        return validation_results

def main():
    """Main function to demonstrate pipeline orchestration."""
    logger.info("Starting A.U.R.A data pipeline orchestration")
    
    # Initialize pipeline orchestrator
    orchestrator = DataPipelineOrchestrator()
    
    # Run complete pipeline
    results = orchestrator.run_complete_pipeline()
    
    # Print results
    print("\n" + "="*60)
    print("A.U.R.A DATA PIPELINE EXECUTION RESULTS")
    print("="*60)
    print(f"Execution ID: {results['execution_id']}")
    print(f"Duration: {results['duration']:.2f} seconds")
    print(f"Overall Success: {orchestrator.pipeline_status['overall_success']}")
    
    if 'statistics' in results:
        stats = results['statistics']
        print(f"\nData Volumes:")
        print(f"  Bronze Records: {stats['bronze_records']:,}")
        print(f"  Silver Records: {stats['silver_records']:,}")
        print(f"  Gold Records: {stats['gold_records']:,}")
    
    if results['errors']:
        print(f"\nErrors ({len(results['errors'])}):")
        for error in results['errors']:
            print(f"  - {error}")
    
    if results['warnings']:
        print(f"\nWarnings ({len(results['warnings'])}):")
        for warning in results['warnings']:
            print(f"  - {warning}")
    
    logger.info("A.U.R.A data pipeline orchestration completed")

if __name__ == "__main__":
    main()

