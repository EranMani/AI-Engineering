# Reliability Guide: Logging, Debugging, and Testing

## Table of Contents

1. [Logging](#1-logging-the-black-box-recorder)
2. [Debugging](#2-debugging-the-surgical-tools)
3. [Testing](#3-testing-the-safety-net)
4. [Best Practices Summary](#best-practices-summary)

---

## 1. Logging: The "Black Box Recorder"

### What is Logging?

Logging is the practice of recording information about your program's execution. Think of it as a "black box recorder" for your code - it tells you **what happened** during execution.

### Why Not Just Use `print()`?

In notebooks, you might write:
```python
print(f"Training epoch {epoch}...")
```

In production AI Engineering, `print()` is dangerous because:

1. **You can't easily turn it off** - All print statements execute, cluttering output
2. **You don't know when or where** - No timestamps, no module names
3. **It doesn't save to a file** - Output is lost when the script finishes
4. **No severity levels** - Everything looks the same

### Logging Levels

Python's `logging` module provides **levels of severity**:

| Level | When to Use | Example |
|-------|-------------|---------|
| **DEBUG** | Detailed information for diagnosing problems | "Loss at step 100: 0.5234" |
| **INFO** | General informational messages about normal operation | "Epoch 1 finished" |
| **WARNING** | Something unexpected happened, but program continues | "GPU temperature high, throttling" |
| **ERROR** | A serious problem occurred, but program can continue | "Data corrupted in batch 42" |
| **CRITICAL** | A serious error occurred, program may not continue | "Out of memory, cannot continue" |

### Quick Quiz Answer

> If you want to track the loss value every 100 steps just to see how training is going, which logging level would that typically be?

**Answer: INFO**

- **DEBUG** would be for very detailed diagnostic information (like individual tensor values)
- **INFO** is for normal progress updates (like loss every 100 steps)
- **ERROR** is for problems that need attention

### Basic Logging Setup

```python
import logging

# Simple setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Use it
logger.info("Training started")
logger.debug("Detailed debug info")  # Won't show with INFO level
logger.warning("Something unusual happened")
logger.error("An error occurred")
```

### Advanced Logging Setup

For production code, use multiple handlers:

```python
import logging
from pathlib import Path

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Console handler - shows INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler - saves everything (DEBUG and above)
    file_handler = logging.FileHandler("training.log")
    file_handler.setLevel(logging.DEBUG)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
```

### Logging Best Practices

1. **Use module-level loggers**: `logger = logging.getLogger(__name__)`
2. **Choose appropriate levels**: Don't use ERROR for normal operations
3. **Include context**: `logger.info(f"Processing batch {batch_id}")`
4. **Use structured logging** for complex data (JSON format)
5. **Log exceptions properly**: `logger.error("Error occurred", exc_info=True)`
6. **Use rotating file handlers** to prevent log files from growing too large

### When to Use Each Level

- **DEBUG**: Development, detailed diagnostics, step-by-step execution
- **INFO**: Normal operation milestones, progress updates, important state changes
- **WARNING**: Recoverable issues, performance concerns, deprecated usage
- **ERROR**: Operation failures, exceptions that are caught and handled
- **CRITICAL**: System-level failures, unrecoverable errors

---

## 2. Debugging: The "Surgical Tools"

### What is Debugging?

Debugging is the process of finding and fixing bugs in your code. It answers the question: **Why did it happen?**

### Debugging Techniques

#### 1. Print Statements (Quick but Limited)

```python
# Old way - not recommended for production
print(f"Value: {value}")
print(f"Type: {type(value)}")
```

**Problems:**
- Hard to remove later
- No severity levels
- Clutters output

#### 2. Logging (Better Alternative)

```python
# Better way
logger.debug(f"Value: {value}, Type: {type(value)}")
logger.info(f"Processing item {i}")
```

**Advantages:**
- Can be turned off by changing log level
- Includes timestamps and context
- Can save to file

#### 3. Assertions

```python
# Catch bugs early
assert len(predictions) == len(targets), "Lengths must match"
assert loss >= 0, "Loss should be non-negative"
```

**Use for:**
- Preconditions (input validation)
- Postconditions (output validation)
- Invariants (things that should always be true)

**Note:** Assertions can be disabled with `python -O`, so don't use them for error handling in production.

#### 4. Python Debugger (pdb)

```python
# Add breakpoint
breakpoint()  # Python 3.7+

# Or use pdb
import pdb; pdb.set_trace()
```

**Common pdb commands:**
- `n` (next): Execute next line
- `s` (step): Step into function
- `c` (continue): Continue execution
- `p variable`: Print variable value
- `l` (list): Show code around current line
- `q` (quit): Exit debugger

#### 5. Try-Except with Detailed Logging

```python
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"ValueError: {e}", exc_info=True)
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
```

### Debugging Strategies

#### Strategy 1: Binary Search
Narrow down where the bug occurs by testing smaller inputs:
1. Start with full dataset
2. Reduce to half
3. Keep narrowing until you find the problematic input

#### Strategy 2: Add Strategic Logging
Add logs at key decision points:
- Function entry/exit
- Loop iterations
- Conditional branches
- Data transformations

#### Strategy 3: Check Your Assumptions
Verify that your assumptions are correct:
- Data types
- Value ranges
- Key existence (for dictionaries)
- List lengths

#### Strategy 4: Isolate the Problem
Create a minimal reproducible example:
- Remove unnecessary code
- Use simple test data
- Focus on the specific bug

### Debugging Workflow

1. **Reproduce the bug**: Can you make it happen consistently?
2. **Add logging**: Add strategic logs around the suspected area
3. **Narrow down**: Use binary search to find the problematic input
4. **Check assumptions**: Verify your assumptions about the data
5. **Use debugger**: Step through code if needed
6. **Fix and verify**: Fix the bug and add a test to prevent regression

---

## 3. Testing: The "Safety Net"

### What is Testing?

Testing is the practice of writing code that verifies your code works correctly. It answers: **Did it break?**

### Why Testing Matters in AI Engineering

In notebooks, "testing" often means:
- Run a cell
- Look at the output
- "Looks right" ✅

In AI Engineering, we need:
- **Automated tests** that run without human intervention
- **Tests that catch regressions** when code changes
- **Tests that verify edge cases** and error handling
- **Tests that run in CI/CD pipelines**

### Types of Tests

#### 1. Unit Tests
Test individual functions or methods in isolation.

```python
def test_calculate_loss():
    predictions = [0.5, 0.7, 0.9]
    targets = [0.4, 0.6, 0.8]
    loss = calculate_loss(predictions, targets)
    assert loss >= 0
    assert isinstance(loss, float)
```

#### 2. Integration Tests
Test how multiple components work together.

```python
def test_training_pipeline():
    data = load_data("train.csv")
    model = train_model(data)
    accuracy = evaluate_model(model, test_data)
    assert accuracy > 0.8
```

#### 3. End-to-End Tests
Test the complete workflow from input to output.

### Writing Good Tests

#### Test Structure (AAA Pattern)

```python
def test_example():
    # Arrange: Set up test data
    predictions = [1.0, 2.0, 3.0]
    targets = [1.0, 2.0, 3.0]
    
    # Act: Execute the code being tested
    loss = calculate_loss(predictions, targets)
    
    # Assert: Verify the result
    assert loss == 0.0
```

#### Test Naming

Use descriptive names that explain what is being tested:

```python
# Good
def test_calculate_loss_returns_zero_for_perfect_predictions():
    ...

# Bad
def test_loss():
    ...
```

#### Test Categories

1. **Happy path**: Normal operation with valid inputs
2. **Edge cases**: Boundary conditions, empty inputs, single items
3. **Error cases**: Invalid inputs, missing data, type errors
4. **Performance**: Large inputs, stress tests

### Testing Tools: pytest

pytest is the most popular testing framework for Python.

#### Installation

```bash
pip install pytest
```

#### Running Tests

```bash
# Run all tests
pytest

# Run specific file
pytest test_file.py

# Run with verbose output
pytest -v

# Run specific test
pytest test_file.py::test_function_name
```

#### pytest Features

**Fixtures**: Reusable test setup

```python
@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_with_fixture(sample_data):
    result = process(sample_data)
    assert len(result) == 5
```

**Parametrized Tests**: Test multiple cases

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected
```

**Markers**: Categorize tests

```python
@pytest.mark.slow
def test_slow_operation():
    ...

# Run only fast tests
pytest -m "not slow"
```

**Mocking**: Replace dependencies

```python
from unittest.mock import Mock

def test_with_mock():
    mock_loader = Mock()
    mock_loader.load.return_value = [1, 2, 3]
    
    data = mock_loader.load("fake_path")
    assert data == [1, 2, 3]
```

### Test Organization

Organize tests to match your code structure:

```
project/
├── src/
│   ├── data_processor.py
│   └── model_trainer.py
└── tests/
    ├── test_data_processor.py
    └── test_model_trainer.py
```

### When to Write Tests

1. **Before fixing a bug**: Write a test that reproduces the bug
2. **After fixing a bug**: Add a test to prevent regression
3. **For new features**: Write tests as you develop
4. **For critical functions**: Always test important logic
5. **For edge cases**: Test boundary conditions

### Test Coverage

Aim for high test coverage, but focus on:
- **Critical paths**: Core business logic
- **Error handling**: Exception cases
- **Edge cases**: Boundary conditions
- **Complex logic**: Difficult algorithms

Don't obsess over 100% coverage - some code (like simple getters) doesn't need tests.

---

## Best Practices Summary

### Logging Best Practices

✅ **DO:**
- Use `logging` module, not `print()`
- Use appropriate log levels
- Include context in log messages
- Use module-level loggers
- Log exceptions with `exc_info=True`
- Use file handlers for production

❌ **DON'T:**
- Use `print()` for production code
- Log sensitive information (passwords, API keys)
- Use ERROR level for normal operations
- Log too frequently (performance impact)

### Debugging Best Practices

✅ **DO:**
- Add strategic logging at key points
- Use assertions for preconditions
- Create minimal reproducible examples
- Use debugger for complex issues
- Check your assumptions
- Document what you tried

❌ **DON'T:**
- Rely only on print statements
- Debug in production code
- Remove debug logs without understanding the issue
- Assume the bug is where you think it is

### Testing Best Practices

✅ **DO:**
- Write tests for new features
- Test edge cases and error conditions
- Use descriptive test names
- Keep tests independent
- Use fixtures for setup
- Run tests before committing

❌ **DON'T:**
- Write tests that depend on each other
- Test implementation details (test behavior)
- Ignore failing tests
- Write tests that are too slow
- Test external dependencies directly (use mocks)

### The Reliability Workflow

1. **Development**: Use DEBUG logging and assertions
2. **Testing**: Write and run tests
3. **Production**: Use INFO/WARNING/ERROR logging
4. **Debugging**: Use logs and debugger when issues occur
5. **Monitoring**: Review logs regularly

---

## Quick Reference

### Logging Quick Reference

```python
import logging

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use
logger.debug("Detailed info")
logger.info("Normal operation")
logger.warning("Something unusual")
logger.error("Error occurred", exc_info=True)
```

### Debugging Quick Reference

```python
# Assertions
assert condition, "Error message"

# Breakpoint
breakpoint()

# Try-except with logging
try:
    code()
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
```

### Testing Quick Reference

```python
import pytest

def test_function():
    # Arrange
    input = [1, 2, 3]
    
    # Act
    result = function(input)
    
    # Assert
    assert result == expected

# Run: pytest test_file.py -v
```

---

## Conclusion

Logging, debugging, and testing are the three pillars of reliable AI Engineering:

- **Logging** tells you what happened
- **Debugging** helps you understand why it happened
- **Testing** ensures it doesn't break

Master these three skills, and you'll be able to build production-ready AI systems with confidence.

Remember: In notebooks, you might get away with `print()` and manual testing. In AI Engineering, you need professional tools and practices.

