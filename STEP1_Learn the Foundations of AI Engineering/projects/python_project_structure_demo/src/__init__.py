"""
Main Package

Demonstrates package structure with __init__.py
"""

from .data_loader import DataLoader
from .model_trainer import ModelTrainer

__all__ = ["DataLoader", "ModelTrainer"]

