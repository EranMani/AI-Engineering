"""
Basic Testing Example
Demonstrates fundamental testing concepts with pytest.
"""

import pytest
from typing import List


def calculate_loss(predictions: List[float], targets: List[float]) -> float:
    """
    Calculate mean squared error.
    
    Args:
        predictions: List of predicted values
        targets: List of target values
    
    Returns:
        Mean squared error
    """
    if len(predictions) != len(targets):
        raise ValueError("Predictions and targets must have the same length")
    
    if len(predictions) == 0:
        raise ValueError("Cannot calculate loss on empty data")
    
    total = sum((p - t) ** 2 for p, t in zip(predictions, targets))
    return total / len(predictions)


# Test 1: Basic functionality test
def test_calculate_loss_basic():
    """Test that loss calculation works for normal inputs."""
    predictions = [0.5, 0.7, 0.9]
    targets = [0.4, 0.6, 0.8]
    
    loss = calculate_loss(predictions, targets)
    
    # Assert that loss is a number
    assert isinstance(loss, float)
    
    # Assert that loss is non-negative
    assert loss >= 0
    
    # Assert expected value (with small tolerance for floating point)
    expected = sum((0.5-0.4)**2, (0.7-0.6)**2, (0.9-0.8)**2) / 3
    assert abs(loss - expected) < 1e-10


# Test 2: Edge case test
def test_calculate_loss_perfect_prediction():
    """Test that loss is zero when predictions match targets exactly."""
    predictions = [1.0, 2.0, 3.0]
    targets = [1.0, 2.0, 3.0]
    
    loss = calculate_loss(predictions, targets)
    
    assert loss == 0.0


# Test 3: Error handling test
def test_calculate_loss_mismatched_lengths():
    """Test that function raises error for mismatched lengths."""
    predictions = [0.5, 0.7]
    targets = [0.4, 0.6, 0.8]
    
    # Use pytest.raises to check that an exception is raised
    with pytest.raises(ValueError, match="must have the same length"):
        calculate_loss(predictions, targets)


# Test 4: Another error case
def test_calculate_loss_empty_input():
    """Test that function raises error for empty input."""
    predictions = []
    targets = []
    
    with pytest.raises(ValueError, match="Cannot calculate loss on empty data"):
        calculate_loss(predictions, targets)


# Test 5: Parameterized test (tests multiple cases at once)
@pytest.mark.parametrize("predictions,targets,expected_loss", [
    ([1.0], [1.0], 0.0),
    ([1.0], [2.0], 1.0),
    ([0.0, 0.0], [1.0, 1.0], 1.0),
    ([1.0, 2.0, 3.0], [1.0, 2.0, 3.0], 0.0),
])
def test_calculate_loss_parametrized(predictions, targets, expected_loss):
    """Test multiple cases using parametrization."""
    loss = calculate_loss(predictions, targets)
    assert abs(loss - expected_loss) < 1e-10


if __name__ == "__main__":
    # Run tests with: pytest basic_testing.py -v
    # Or run this file directly
    pytest.main([__file__, "-v"])

