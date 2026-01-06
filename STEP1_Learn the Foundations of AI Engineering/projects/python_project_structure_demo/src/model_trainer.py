"""
Model Trainer Module

Demonstrates how modules import from the same package.
"""

from typing import Optional
import pandas as pd
from .data_loader import DataLoader


class ModelTrainer:
    """Trains models using data from DataLoader."""
    
    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.data_loader = data_loader or DataLoader()
    
    def train(self, data: pd.DataFrame) -> dict:
        """Train a model on the provided data."""
        return {
            "accuracy": 0.95,
            "loss": 0.05,
            "epochs": 10
        }

