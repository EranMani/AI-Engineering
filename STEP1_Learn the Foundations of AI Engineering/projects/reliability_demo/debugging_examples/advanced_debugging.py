"""
Advanced Debugging Example
Demonstrates pdb, breakpoints, and debugging strategies.
"""

import logging
import sys
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_batch(data: List[Dict], batch_size: int = 10):
    """
    Example function that processes data in batches.
    Demonstrates debugging techniques.
    """
    logger.info(f"Processing {len(data)} items in batches of {batch_size}")
    
    results = []
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        logger.debug(f"Processing batch {i // batch_size + 1}: {len(batch)} items")
        
        # Simulate processing
        batch_result = []
        for item in batch:
            # Potential bug: what if 'value' key doesn't exist?
            processed = item.get('value', 0) * 2
            batch_result.append(processed)
        
        results.extend(batch_result)
        logger.debug(f"Batch processed. Results: {batch_result[:3]}...")  # Show first 3
    
    return results


def debug_with_pdb_example():
    """
    Demonstrates using Python debugger (pdb).
    
    To use pdb:
    1. Add: import pdb; pdb.set_trace() where you want to break
    2. Or use: breakpoint() in Python 3.7+
    3. Commands:
       - n (next line)
       - s (step into function)
       - c (continue)
       - p variable_name (print variable)
       - l (list code)
       - q (quit)
    """
    logger.info("=" * 50)
    logger.info("Debugging with pdb/breakpoint()")
    logger.info("=" * 50)
    logger.info("Uncomment breakpoint() in code to use interactive debugger")
    
    data = [
        {'value': 1, 'id': 1},
        {'value': 2, 'id': 2},
        {'value': 3, 'id': 3},
    ]
    
    # Uncomment the line below to start interactive debugging
    # breakpoint()  # Python 3.7+ way, or use: import pdb; pdb.set_trace()
    
    results = process_batch(data, batch_size=2)
    logger.info(f"Final results: {results}")


def debug_with_try_except():
    """Using try-except for defensive programming and debugging."""
    logger.info("=" * 50)
    logger.info("Debugging with try-except")
    logger.info("=" * 50)
    
    def safe_process_batch(data: List[Dict], batch_size: int = 10):
        """Version with error handling."""
        results = []
        
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            
            try:
                batch_result = []
                for item in batch:
                    # More defensive: check if key exists
                    if 'value' not in item:
                        logger.warning(f"Item missing 'value' key: {item}")
                        continue
                    
                    processed = item['value'] * 2
                    batch_result.append(processed)
                
                results.extend(batch_result)
                logger.debug(f"Batch {i // batch_size + 1} processed successfully")
                
            except KeyError as e:
                logger.error(f"KeyError in batch {i // batch_size + 1}: {e}", exc_info=True)
                raise
            except Exception as e:
                logger.error(f"Unexpected error in batch {i // batch_size + 1}: {e}", exc_info=True)
                raise
        
        return results
    
    # Test with good data
    good_data = [{'value': i} for i in range(5)]
    results = safe_process_batch(good_data)
    logger.info(f"Processed {len(results)} items successfully")
    
    # Test with bad data (missing key)
    bad_data = [{'value': 1}, {'id': 2}, {'value': 3}]
    try:
        results = safe_process_batch(bad_data)
    except Exception as e:
        logger.error(f"Processing failed: {e}")


def debug_with_inspection():
    """Using introspection to understand code state."""
    logger.info("=" * 50)
    logger.info("Debugging with introspection")
    logger.info("=" * 50)
    
    def inspect_function(func):
        """Inspect a function's properties."""
        logger.info(f"Function name: {func.__name__}")
        logger.info(f"Function docstring: {func.__doc__}")
        logger.info(f"Function code: {func.__code__.co_filename}:{func.__code__.co_firstlineno}")
        logger.info(f"Number of arguments: {func.__code__.co_argcount}")
        logger.info(f"Argument names: {func.__code__.co_varnames[:func.__code__.co_argcount]}")
    
    inspect_function(process_batch)
    
    # Inspect variables
    data = [{'value': i} for i in range(3)]
    logger.debug(f"Data type: {type(data)}")
    logger.debug(f"Data length: {len(data)}")
    logger.debug(f"Data structure: {data}")
    logger.debug(f"First item type: {type(data[0])}")
    logger.debug(f"First item keys: {data[0].keys() if isinstance(data[0], dict) else 'N/A'}")


if __name__ == "__main__":
    debug_with_pdb_example()
    print()
    debug_with_try_except()
    print()
    debug_with_inspection()

