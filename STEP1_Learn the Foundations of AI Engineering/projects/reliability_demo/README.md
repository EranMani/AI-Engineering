# Reliability Demo: Logging, Debugging, and Testing

This demo folder demonstrates the "Big Three" of reliability in AI Engineering:

1. **Logging**: The "Black Box Recorder" (What happened?)
2. **Debugging**: The "Surgical Tools" (Why did it happen?)
3. **Testing**: The "Safety Net" (Did it break?)

## Quick Start

```bash
# Navigate to the demo folder
cd reliability_demo

# Run logging examples
python logging_examples/basic_logging.py
python logging_examples/advanced_logging.py
python logging_examples/logging_best_practices.py

# Run debugging examples
python debugging_examples/basic_debugging.py
python debugging_examples/advanced_debugging.py
python debugging_examples/debugging_strategies.py

# Run tests
pytest testing_examples/ -v
```

## Structure

```
reliability_demo/
├── logging_examples/      # Logging demonstrations
├── debugging_examples/    # Debugging techniques
├── testing_examples/      # Testing examples
└── README.md             # This file
```

## See Also

For detailed explanations and best practices, see [RELIABILITY_GUIDE.md](RELIABILITY_GUIDE.md).

