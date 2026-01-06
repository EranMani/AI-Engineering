"""
Basic Logging Example
Demonstrates the fundamental concepts of Python logging.
"""

import logging

# Basic setup - this is the simplest way to start logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Get a logger for this module
logger = logging.getLogger(__name__)


def train_model_simple():
    """Simulates a simple training loop with logging."""
    logger.info("Starting model training...")
    
    for epoch in range(1, 4):
        logger.info(f"Epoch {epoch} started")
        # Simulate training
        loss = 1.0 / epoch
        logger.debug(f"Loss at step 100: {loss:.4f}")  # This won't show with INFO level
        logger.info(f"Epoch {epoch} finished with loss: {loss:.4f}")
    
    logger.info("Training completed successfully")


if __name__ == "__main__":
    train_model_simple()

