"""
Advanced Testing Example
Demonstrates fixtures, mocking, and integration tests.
"""

import pytest
import tempfile
import json
from pathlib import Path
from typing import List, Dict
from unittest.mock import Mock, patch, MagicMock


# Example class to test
class ModelTrainer:
    """Simple model trainer for testing demonstration."""
    
    def __init__(self, learning_rate: float = 0.001):
        self.learning_rate = learning_rate
        self.epochs_trained = 0
        self.loss_history = []
    
    def train_epoch(self, data: List[float]) -> float:
        """Train for one epoch and return loss."""
        # Simulate training
        loss = sum(data) / len(data) if data else 0.0
        self.loss_history.append(loss)
        self.epochs_trained += 1
        return loss
    
    def save_model(self, path: Path):
        """Save model to file."""
        model_data = {
            'learning_rate': self.learning_rate,
            'epochs_trained': self.epochs_trained,
            'loss_history': self.loss_history
        }
        with open(path, 'w') as f:
            json.dump(model_data, f)
    
    def load_model(self, path: Path):
        """Load model from file."""
        with open(path, 'r') as f:
            model_data = json.load(f)
        self.learning_rate = model_data['learning_rate']
        self.epochs_trained = model_data['epochs_trained']
        self.loss_history = model_data['loss_history']


# Fixture: Reusable test data
@pytest.fixture
def sample_data():
    """Provide sample training data."""
    return [0.1, 0.2, 0.3, 0.4, 0.5]


# Fixture: Create a trainer instance
@pytest.fixture
def trainer():
    """Create a fresh trainer instance for each test."""
    return ModelTrainer(learning_rate=0.001)


# Fixture: Temporary directory for file operations
@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# Test using fixtures
def test_train_epoch_basic(trainer, sample_data):
    """Test training one epoch using fixtures."""
    loss = trainer.train_epoch(sample_data)
    
    assert loss == pytest.approx(0.3)  # (0.1+0.2+0.3+0.4+0.5)/5
    assert trainer.epochs_trained == 1
    assert len(trainer.loss_history) == 1


def test_train_multiple_epochs(trainer, sample_data):
    """Test training multiple epochs."""
    losses = []
    for _ in range(3):
        loss = trainer.train_epoch(sample_data)
        losses.append(loss)
    
    assert trainer.epochs_trained == 3
    assert len(trainer.loss_history) == 3
    assert all(l == pytest.approx(0.3) for l in losses)


# Test file operations
def test_save_and_load_model(trainer, sample_data, temp_dir):
    """Test saving and loading model."""
    # Train the model
    trainer.train_epoch(sample_data)
    trainer.train_epoch(sample_data)
    
    # Save model
    model_path = temp_dir / "model.json"
    trainer.save_model(model_path)
    
    # Verify file exists
    assert model_path.exists()
    
    # Create new trainer and load
    new_trainer = ModelTrainer()
    new_trainer.load_model(model_path)
    
    # Verify loaded state
    assert new_trainer.learning_rate == trainer.learning_rate
    assert new_trainer.epochs_trained == trainer.epochs_trained
    assert new_trainer.loss_history == trainer.loss_history


# Mocking example
def test_with_mocking():
    """Demonstrate mocking external dependencies."""
    
    # Create a mock object
    mock_data_loader = Mock()
    mock_data_loader.load.return_value = [1.0, 2.0, 3.0]
    
    # Use the mock
    data = mock_data_loader.load("fake_path.csv")
    
    # Verify mock was called
    mock_data_loader.load.assert_called_once_with("fake_path.csv")
    assert data == [1.0, 2.0, 3.0]


# Patching example
@patch('builtins.open', create=True)
def test_file_operations_with_patch(mock_open):
    """Demonstrate patching file operations."""
    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file
    mock_file.read.return_value = '{"test": "data"}'
    
    # Code that uses open()
    with open('test.json', 'r') as f:
        data = json.loads(f.read())
    
    # Verify the mock was called
    mock_open.assert_called_once_with('test.json', 'r')
    assert data == {"test": "data"}


# Integration test example
def test_full_training_pipeline(trainer, sample_data, temp_dir):
    """Integration test: test the full workflow."""
    # Step 1: Train model
    for _ in range(5):
        trainer.train_epoch(sample_data)
    
    assert trainer.epochs_trained == 5
    
    # Step 2: Save model
    model_path = temp_dir / "trained_model.json"
    trainer.save_model(model_path)
    assert model_path.exists()
    
    # Step 3: Load and verify
    loaded_trainer = ModelTrainer()
    loaded_trainer.load_model(model_path)
    
    assert loaded_trainer.epochs_trained == 5
    assert len(loaded_trainer.loss_history) == 5


# Test with different configurations
@pytest.mark.parametrize("learning_rate,expected", [
    (0.001, 0.001),
    (0.01, 0.01),
    (0.1, 0.1),
])
def test_trainer_initialization(learning_rate, expected):
    """Test trainer with different learning rates."""
    trainer = ModelTrainer(learning_rate=learning_rate)
    assert trainer.learning_rate == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

