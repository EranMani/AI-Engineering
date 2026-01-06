"""
Advanced Logging Example
Demonstrates file logging, multiple handlers, and log levels.
"""

import logging
import logging.handlers
import os
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)


def setup_advanced_logger(name: str = __name__):
    """
    Sets up an advanced logger with:
    - Console handler (INFO level)
    - File handler (DEBUG level - captures everything)
    - Rotating file handler (prevents log files from growing too large)
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all levels
    
    # Prevent duplicate logs if handler already exists
    if logger.handlers:
        return logger
    
    # Console handler - shows INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # File handler - saves everything (DEBUG and above)
    file_handler = logging.FileHandler(log_dir / "training.log")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    # Rotating file handler - keeps last 5 files, max 1MB each
    rotating_handler = logging.handlers.RotatingFileHandler(
        log_dir / "training_rotating.log",
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    rotating_handler.setLevel(logging.DEBUG)
    rotating_handler.setFormatter(file_format)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(rotating_handler)
    
    return logger


def train_model_advanced():
    """Simulates training with different log levels."""
    logger = setup_advanced_logger(__name__)
    
    logger.info("=" * 50)
    logger.info("Starting advanced model training")
    logger.info("=" * 50)
    
    try:
        for epoch in range(1, 6):
            logger.info(f"Epoch {epoch} started")
            
            # Simulate training steps
            for step in range(1, 101):
                loss = 1.0 / (epoch * step)
                
                # DEBUG: Detailed information (only in file)
                if step % 10 == 0:
                    logger.debug(f"Step {step}: loss={loss:.6f}, lr=0.001")
                
                # INFO: Important milestones (console + file)
                if step % 50 == 0:
                    logger.info(f"Step {step}: loss={loss:.4f}")
            
            # WARNING: Something unusual but not critical
            if epoch == 3:
                logger.warning("GPU temperature is high (75°C), but continuing...")
            
            logger.info(f"Epoch {epoch} completed")
        
        logger.info("Training completed successfully")
        
    except Exception as e:
        # ERROR: Something went wrong
        logger.error(f"Training failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    train_model_advanced()
    print(f"\nCheck the logs directory for detailed logs: {log_dir.absolute()}")

