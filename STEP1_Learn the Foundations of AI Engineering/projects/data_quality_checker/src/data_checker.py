"""
Data Quality Checker
A tool for validating data quality in CSV files.
"""

import logging
import pandas as pd
from pathlib import Path
from typing import List,Dict,Any
from collections import defaultdict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

class DataQualityChecker:
    """Main class for checking data quality."""
    
    def __init__(self):
        """Initialize the data quality checker."""
        logger.info("Initializing DataQualityChecker")
        self.data = None
        self.issues = defaultdict(list)
        logger.debug("DataQualityChecker initialized successfully")
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load data from a CSV file using pandas.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            pandas DataFrame containing the loaded data
        """
        logger.info(f"Loading data from: {file_path}")

        file_path_obj = Path(file_path)

        if not file_path_obj.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.debug(f"File exists. Size: {file_path_obj.stat().st_size} bytes")

        try:
            df = pd.read_csv(file_path)
            logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns from {file_path}")
            logger.debug(f"Columns: {list(df.columns)}")
            logger.debug(f"Data shape: {df.shape}")
            logger.debug(f"Data types:\n {df.dtypes}")

            self.data = df
            return df
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}", exc_info=True)
            raise
    
    def check_missing_values(self) -> Dict[str, int]:
        """
        Check for missing values in the data using pandas.
        
        Returns:
            Dictionary mapping column names to count of missing values
        """
        logger.info("Checking for missing values")

        if self.data is None:
            logger.warning("No data loaded. Call load_data() first.")
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Use pandas to count missing values
        missing_counts = self.data.isnull().sum().to_dict()

        for col, count in missing_counts.items():
            if count > 0:
                logger.warning(f"Column '{col}' has {count} missing values ({count/len(self.data)*100:.1f}%)")
                self.issues["missing_values"].append({
                    'column': col,
                    'count': int(count),
                    'percentage': count/len(self.data)*100
                })
            else:
                logger.debug(f"Column '{col}' has no missing values")

        total_missing = sum(missing_counts.values())
        logger.info(f"Missing value check complete. Total missing: {total_missing}")
        
        return missing_counts
    
    def generate_report(self) -> str:
        """
        Generate a quality report.
        
        Returns:
            String containing the quality report
        """
        logger.info("Generating quality report")

        if self.data is None:
            logger.warning("No data loaded. Cannot generate report")
            return "No data loaded"

        report_lines = []
        report_lines.append("=" * 50)
        report_lines.append("DATA QUALITY REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Total rows: {len(self.data)}")
        report_lines.append(f"Total columns: {len(self.data.columns)}")
        report_lines.append("")
        
        # Missing values section
        if 'missing_values' in self.issues:
            report_lines.append("MISSING VALUES:")
            for issue in self.issues['missing_values']:
                report_lines.append(
                    f"  - {issue['column']}: {issue['count']} missing ({issue['percentage']:.1f}%)"
                )
        else:
            report_lines.append("MISSING VALUES: None found")
        
        report_lines.append("")
        report_lines.append("=" * 50)
        
        report = "\n".join(report_lines)
        logger.info("Quality report generated successfully")
        logger.debug(f"Report content:\n{report}")
        
        return report