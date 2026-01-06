"""
Logging Best Practices Example
Shows proper logging patterns for AI/ML workflows.
"""

import logging
from pathlib import Path
from typing import Optional

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Example class showing logging best practices:
    1. Use module-level loggers (not root logger)
    2. Log at appropriate levels
    3. Include context in messages
    4. Use structured logging for complex data
    """
    
    def __init__(self, model_name: str, log_dir: Optional[Path] = None):
        self.model_name = model_name
        self.log_dir = log_dir or Path("logs")
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info(f"Initialized {self.__class__.__name__} for model: {model_name}")
    
    def load_data(self, data_path: str):
        """Load training data with logging."""
        self.logger.info(f"Loading data from {data_path}")
        try:
            # Simulate data loading
            data_size = 10000
            self.logger.debug(f"Data shape: {data_size} samples")
            self.logger.info(f"Successfully loaded {data_size} samples")
            return data_size
        except FileNotFoundError:
            self.logger.error(f"Data file not found: {data_path}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error loading data: {e}", exc_info=True)
            raise
    
    def train(self, epochs: int = 10):
        """Train model with detailed logging."""
        self.logger.info(f"Starting training for {epochs} epochs")
        
        for epoch in range(1, epochs + 1):
            self.logger.info(f"Epoch {epoch}/{epochs}")
            
            # Log metrics at appropriate intervals
            metrics = {
                "loss": 1.0 / epoch,
                "accuracy": 0.5 + (epoch * 0.05),
                "learning_rate": 0.001
            }
            
            # Use INFO for important metrics
            self.logger.info(
                f"Metrics - Loss: {metrics['loss']:.4f}, "
                f"Accuracy: {metrics['accuracy']:.4f}, "
                f"LR: {metrics['learning_rate']}"
            )
            
            # Use DEBUG for detailed information
            self.logger.debug(f"Full metrics dict: {metrics}")
            
            # WARNING for concerning but non-fatal issues
            if metrics['loss'] > 0.5:
                self.logger.warning(f"Loss is high ({metrics['loss']:.4f}), consider adjusting learning rate")
        
        self.logger.info("Training completed successfully")
    
    def evaluate(self, test_data_size: int = 1000):
        """Evaluate model with logging."""
        self.logger.info(f"Evaluating on {test_data_size} test samples")
        
        # Simulate evaluation
        accuracy = 0.85
        self.logger.info(f"Test accuracy: {accuracy:.2%}")
        
        if accuracy < 0.8:
            self.logger.warning(f"Accuracy ({accuracy:.2%}) is below target (80%)")
        
        return accuracy


def demonstrate_best_practices():
    """Demonstrates logging best practices."""
    logger.info("=" * 60)
    logger.info("Logging Best Practices Demonstration")
    logger.info("=" * 60)
    
    trainer = ModelTrainer("my_model")
    
    try:
        data_size = trainer.load_data("data/train.csv")
        trainer.train(epochs=5)
        trainer.evaluate(test_data_size=1000)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)


if __name__ == "__main__":
    demonstrate_best_practices()

