"""
Example: Using the Package

Shows how to use the package from outside the package directory.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import using absolute imports
from src import DataLoader, ModelTrainer

# Use the package
loader = DataLoader()
trainer = ModelTrainer(loader)

print("✓ Package imported and used successfully!")
print(f"  DataLoader: {loader}")
print(f"  ModelTrainer: {trainer}")

