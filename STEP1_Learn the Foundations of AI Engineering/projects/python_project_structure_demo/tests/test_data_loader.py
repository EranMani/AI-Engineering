"""
Test module for DataLoader

Demonstrates how to structure tests in a Python project.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader import DataLoader


def test_data_loader_initialization():
    """Test DataLoader initialization."""
    loader = DataLoader()
    assert loader is not None
    assert loader.data_dir == Path("data")


def test_data_loader_custom_dir():
    """Test DataLoader with custom directory."""
    custom_dir = Path("custom_data")
    loader = DataLoader(data_dir=custom_dir)
    assert loader.data_dir == custom_dir

