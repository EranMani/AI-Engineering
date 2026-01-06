"""
Data Loader Module

Demonstrates a simple module structure.
"""

import pandas as pd
from pathlib import Path
from typing import Optional


class DataLoader:
    """Handles loading and preprocessing data."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path("data")
    
    def load_csv(self, filename: str) -> pd.DataFrame:
        """Load a CSV file."""
        filepath = self.data_dir / filename
        return pd.read_csv(filepath)
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the data."""
        return df.dropna()

