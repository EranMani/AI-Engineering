"""
Test Organization Example
Shows how to organize tests for a real project.
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path for imports (in real project, use proper package structure)
sys.path.insert(0, str(Path(__file__).parent.parent))

# Example module to test (simulated)
class DataProcessor:
    """Example class representing a data processing module."""
    
    def __init__(self):
        self.processed_count = 0
    
    def process(self, data: list) -> list:
        """Process data and return results."""
        self.processed_count += len(data)
        return [x * 2 for x in data]
    
    def reset(self):
        """Reset the processor state."""
        self.processed_count = 0


class ModelEvaluator:
    """Example class representing a model evaluation module."""
    
    @staticmethod
    def calculate_accuracy(predictions: list, targets: list) -> float:
        """Calculate accuracy."""
        if len(predictions) != len(targets):
            raise ValueError("Lengths must match")
        
        correct = sum(1 for p, t in zip(predictions, targets) if p == t)
        return correct / len(predictions) if predictions else 0.0


# Test classes organize related tests
class TestDataProcessor:
    """Group of tests for DataProcessor."""
    
    def test_process_basic(self):
        """Test basic processing functionality."""
        processor = DataProcessor()
        data = [1, 2, 3]
        result = processor.process(data)
        assert result == [2, 4, 6]
        assert processor.processed_count == 3
    
    def test_process_empty(self):
        """Test processing empty data."""
        processor = DataProcessor()
        result = processor.process([])
        assert result == []
        assert processor.processed_count == 0
    
    def test_reset(self):
        """Test reset functionality."""
        processor = DataProcessor()
        processor.process([1, 2, 3])
        assert processor.processed_count == 3
        
        processor.reset()
        assert processor.processed_count == 0


class TestModelEvaluator:
    """Group of tests for ModelEvaluator."""
    
    def test_calculate_accuracy_perfect(self):
        """Test accuracy calculation with perfect predictions."""
        predictions = [1, 2, 3]
        targets = [1, 2, 3]
        accuracy = ModelEvaluator.calculate_accuracy(predictions, targets)
        assert accuracy == 1.0
    
    def test_calculate_accuracy_partial(self):
        """Test accuracy calculation with partial correctness."""
        predictions = [1, 2, 3]
        targets = [1, 2, 4]
        accuracy = ModelEvaluator.calculate_accuracy(predictions, targets)
        assert accuracy == pytest.approx(2/3)
    
    def test_calculate_accuracy_mismatched_lengths(self):
        """Test that mismatched lengths raise error."""
        predictions = [1, 2]
        targets = [1, 2, 3]
        
        with pytest.raises(ValueError, match="Lengths must match"):
            ModelEvaluator.calculate_accuracy(predictions, targets)


# Fixtures can be shared across test classes
@pytest.fixture
def sample_data():
    """Shared fixture for sample data."""
    return [1, 2, 3, 4, 5]


class TestIntegration:
    """Integration tests that test multiple components together."""
    
    def test_full_pipeline(self, sample_data):
        """Test complete data processing and evaluation pipeline."""
        # Process data
        processor = DataProcessor()
        processed = processor.process(sample_data)
        
        # Evaluate (using processed as predictions, original as targets)
        # This is just for demonstration
        accuracy = ModelEvaluator.calculate_accuracy(
            processed, 
            [x * 2 for x in sample_data]  # Expected processed result
        )
        
        assert accuracy == 1.0
        assert processor.processed_count == len(sample_data)


# Markers for categorizing tests
@pytest.mark.slow
def test_slow_operation():
    """Example of a slow test that can be skipped."""
    import time
    time.sleep(0.1)  # Simulate slow operation
    assert True


@pytest.mark.unit
def test_unit_test():
    """Example unit test marker."""
    processor = DataProcessor()
    assert processor.processed_count == 0


@pytest.mark.integration
def test_integration_test():
    """Example integration test marker."""
    processor = DataProcessor()
    evaluator = ModelEvaluator()
    
    data = [1, 2, 3]
    processed = processor.process(data)
    # Integration test logic here
    assert len(processed) == len(data)


if __name__ == "__main__":
    # Run with markers: pytest test_organization.py -m "not slow" -v
    pytest.main([__file__, "-v"])

