"""
Debugging Strategies Example
Shows systematic approaches to finding and fixing bugs.
"""

import logging
from typing import List, Optional

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Example class with a bug for debugging demonstration.
    Shows systematic debugging approach.
    """
    
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.processed_count = 0
        logger.info(f"Initialized DataProcessor with threshold={threshold}")
    
    def process_item(self, value: float) -> Optional[float]:
        """
        Process a single item.
        BUG: Doesn't handle negative values correctly.
        """
        logger.debug(f"Processing item: {value}")
        
        # BUG: This will fail for negative values
        if value > self.threshold:
            result = value * 2
            self.processed_count += 1
            logger.debug(f"Item processed: {value} -> {result}")
            return result
        else:
            logger.debug(f"Item below threshold: {value}")
            return None
    
    def process_batch(self, values: List[float]) -> List[float]:
        """Process a batch of values."""
        logger.info(f"Processing batch of {len(values)} items")
        results = []
        
        for i, value in enumerate(values):
            logger.debug(f"Processing item {i+1}/{len(values)}: {value}")
            result = self.process_item(value)
            if result is not None:
                results.append(result)
        
        logger.info(f"Batch processed: {len(results)}/{len(values)} items passed threshold")
        return results


def strategy_1_binary_search():
    """
    Strategy 1: Binary Search
    Narrow down where the bug occurs by testing smaller inputs.
    """
    logger.info("=" * 60)
    logger.info("Strategy 1: Binary Search - Narrow down the problem")
    logger.info("=" * 60)
    
    processor = DataProcessor(threshold=0.5)
    
    # Start with a large dataset
    large_data = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    logger.info(f"Testing with {len(large_data)} items")
    results = processor.process_batch(large_data)
    logger.info(f"Results: {len(results)} items")
    
    # Narrow down: test with just one item
    single_item = [0.6]
    logger.info(f"Testing with single item: {single_item}")
    results = processor.process_batch(single_item)
    logger.info(f"Results: {results}")
    
    # Test edge case
    edge_case = [0.5]  # Exactly at threshold
    logger.info(f"Testing edge case: {edge_case}")
    results = processor.process_batch(edge_case)
    logger.info(f"Results: {results}")


def strategy_2_add_logging():
    """
    Strategy 2: Add Strategic Logging
    Add logs at key decision points to trace execution.
    """
    logger.info("=" * 60)
    logger.info("Strategy 2: Add Strategic Logging")
    logger.info("=" * 60)
    
    processor = DataProcessor(threshold=0.5)
    
    # Test with problematic input
    test_data = [-0.5, 0.0, 0.5, 1.0]
    logger.info(f"Testing with data: {test_data}")
    
    # Enable detailed logging
    for value in test_data:
        logger.info(f"--- Processing value: {value} ---")
        logger.debug(f"Value type: {type(value)}")
        logger.debug(f"Threshold: {processor.threshold}")
        logger.debug(f"Comparison: {value} > {processor.threshold} = {value > processor.threshold}")
        
        result = processor.process_item(value)
        logger.info(f"Result: {result}")
        logger.info("")


def strategy_3_check_assumptions():
    """
    Strategy 3: Check Your Assumptions
    Verify that your assumptions about the data are correct.
    """
    logger.info("=" * 60)
    logger.info("Strategy 3: Check Your Assumptions")
    logger.info("=" * 60)
    
    def safe_process_item(processor: DataProcessor, value: float) -> Optional[float]:
        """Version that checks assumptions."""
        logger.debug(f"Processing: {value}")
        
        # Check assumptions
        if not isinstance(value, (int, float)):
            logger.error(f"Assumption violated: value is not numeric: {type(value)}")
            return None
        
        if value < 0:
            logger.warning(f"Assumption violated: negative value encountered: {value}")
            # Handle negative values
            return None
        
        # Original logic
        if value > processor.threshold:
            result = value * 2
            processor.processed_count += 1
            return result
        return None
    
    processor = DataProcessor(threshold=0.5)
    
    # Test with various inputs
    test_cases = [
        (0.6, "Normal case"),
        (0.5, "Edge case (at threshold)"),
        (0.4, "Below threshold"),
        (-0.5, "Negative value"),
        (0.0, "Zero"),
    ]
    
    for value, description in test_cases:
        logger.info(f"Test: {description} - value={value}")
        result = safe_process_item(processor, value)
        logger.info(f"  Result: {result}")
        logger.info("")


def strategy_4_isolate_problem():
    """
    Strategy 4: Isolate the Problem
    Create a minimal reproducible example.
    """
    logger.info("=" * 60)
    logger.info("Strategy 4: Isolate the Problem - Minimal Example")
    logger.info("=" * 60)
    
    # Minimal example that reproduces the bug
    threshold = 0.5
    value = -0.3
    
    logger.info(f"Minimal example:")
    logger.info(f"  threshold = {threshold}")
    logger.info(f"  value = {value}")
    logger.info(f"  value > threshold = {value > threshold}")
    
    # The bug: negative values pass the comparison but shouldn't be processed
    if value > threshold:
        result = value * 2
        logger.info(f"  Result: {result}")
    else:
        logger.info(f"  Result: None (below threshold)")
    
    logger.info("")
    logger.info("Issue: Negative values shouldn't be processed, but the")
    logger.info("       comparison 'value > threshold' is True for some negatives!")


if __name__ == "__main__":
    strategy_1_binary_search()
    print()
    strategy_2_add_logging()
    print()
    strategy_3_check_assumptions()
    print()
    strategy_4_isolate_problem()

