"""
Example: Absolute Imports

Absolute imports start from the package name.
They're explicit and work from anywhere in your project.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Absolute imports: explicit and clear
from src.data_loader import DataLoader
from src.model_trainer import ModelTrainer

# Or use package-level imports from __init__.py
from src import DataLoader, ModelTrainer

# Use the imports
loader = DataLoader()
trainer = ModelTrainer(loader)

print("✓ Absolute imports work!")
print(f"  DataLoader: {loader}")
print(f"  ModelTrainer: {trainer}")

