"""
Basic Debugging Example
Demonstrates fundamental debugging techniques.
"""

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def calculate_loss(predictions, targets):
    """
    Example function with intentional bug for debugging demonstration.
    """
    # BUG: Missing check for empty lists
    total = sum((p - t) ** 2 for p, t in zip(predictions, targets))
    mean_loss = total / len(predictions)
    return mean_loss


def debug_with_print():
    """Old way: using print statements (not recommended)."""
    print("=" * 50)
    print("Debugging with print() - NOT RECOMMENDED")
    print("=" * 50)
    
    predictions = [0.5, 0.7, 0.9]
    targets = [0.4, 0.6, 0.8]
    
    print(f"Predictions: {predictions}")
    print(f"Targets: {targets}")
    
    loss = calculate_loss(predictions, targets)
    print(f"Loss: {loss}")


def debug_with_logging():
    """Better way: using logging (recommended)."""
    logger.info("=" * 50)
    logger.info("Debugging with logging - RECOMMENDED")
    logger.info("=" * 50)
    
    predictions = [0.5, 0.7, 0.9]
    targets = [0.4, 0.6, 0.8]
    
    logger.debug(f"Input - Predictions: {predictions}")
    logger.debug(f"Input - Targets: {targets}")
    logger.debug(f"Length check - Predictions: {len(predictions)}, Targets: {len(targets)}")
    
    loss = calculate_loss(predictions, targets)
    logger.info(f"Calculated loss: {loss:.4f}")


def debug_with_assertions():
    """Using assertions to catch bugs early."""
    logger.info("=" * 50)
    logger.info("Debugging with assertions")
    logger.info("=" * 50)
    
    predictions = [0.5, 0.7, 0.9]
    targets = [0.4, 0.6, 0.8]
    
    # Assertions help catch bugs during development
    assert len(predictions) == len(targets), "Predictions and targets must have same length"
    assert len(predictions) > 0, "Cannot calculate loss on empty data"
    
    loss = calculate_loss(predictions, targets)
    assert loss >= 0, "Loss should be non-negative"
    
    logger.info(f"Loss calculated successfully: {loss:.4f}")


if __name__ == "__main__":
    debug_with_print()
    print()
    debug_with_logging()
    print()
    debug_with_assertions()

