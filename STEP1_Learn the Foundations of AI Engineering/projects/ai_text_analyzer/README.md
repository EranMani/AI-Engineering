# AI Text Analyzer - Complete Foundation Project

A comprehensive AI-powered text analysis CLI tool that demonstrates all foundational AI engineering concepts. This project serves as a complete template for building production-ready AI applications with clean code structure, proper error handling, logging, testing, and modern dependency management.

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Complete Guide: Building an AI Project from Scratch](#complete-guide-building-an-ai-project-from-scratch)
4. [Project Structure Explained](#project-structure-explained)
5. [Key Concepts Deep Dive](#key-concepts-deep-dive)
6. [Usage Examples](#usage-examples)
7. [Testing](#testing)
8. [Best Practices](#best-practices)

---

## Project Overview

This project demonstrates:

- ✅ **Clean Project Structure** - Proper Python package organization
- ✅ **Modern Dependency Management** - Using `uv` and `pyproject.toml`
- ✅ **Environment Variables** - Secure API key management
- ✅ **Comprehensive Logging** - File and console handlers
- ✅ **Error Handling** - Retry logic with tenacity
- ✅ **Type Safety** - Pydantic models for structured outputs
- ✅ **Testing** - Unit tests with mocking
- ✅ **OpenAI API Integration** - Modern `responses.parse()` API
- ✅ **Prompt Engineering** - System prompts and user prompts

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key

### Installation

1. **Clone or navigate to the project:**
   ```bash
   cd ai_text_analyzer
   ```

2. **Create virtual environment and install dependencies:**
   ```bash
   uv sync --extra dev
   ```

3. **Set up environment variables:**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

4. **Run the application:**
   ```bash
   python main.py analyze --text "I'm feeling great today!"
   ```

---

## Complete Guide: Building an AI Project from Scratch

This section provides a step-by-step guide to create a professional AI project from scratch, explaining each step and its importance.

### Step 1: Project Structure Setup

**Why it matters:** A well-organized project structure makes your code maintainable, testable, and scalable. It separates concerns and makes collaboration easier.

**Create the following directory structure:**

```
your_ai_project/
├── src/                    # Main source code package
│   ├── __init__.py        # Makes src a Python package
│   ├── your_module.py     # Your main logic
│   └── ...
├── tests/                  # Test package
│   ├── __init__.py        # Makes tests a package
│   ├── test_your_module.py # Your tests
│   └── ...
├── data/                   # Data files (optional)
├── logs/                   # Log files (auto-created)
├── .env                    # Environment variables (gitignored)
├── .env.example            # Template for .env
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Project configuration
├── uv.lock                 # Lock file (auto-generated)
├── README.md               # Project documentation
└── main.py                 # Entry point
```

**Key Points:**
- `src/` separates your source code from other files
- `tests/` mirrors your source structure for easy navigation
- `__init__.py` files make directories Python packages
- Separate directories for data, logs, etc. keep things organized

**Example `__init__.py`:**
```python
# src/__init__.py
# Can be empty or export main classes/functions
from .your_module import YourClass

__all__ = ["YourClass"]
```

---

### Step 2: Dependency Management with `uv` and `pyproject.toml`

**Why it matters:** Modern dependency management ensures reproducible builds, version control, and easy collaboration. `uv` is faster and more reliable than traditional `pip`.

**Create `pyproject.toml`:**

```toml
[project]
name = "your-ai-project"
version = "0.1.0"
description = "Your project description"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "openai>=2.14.0",      # OpenAI API client
    "pydantic>=2.12.5",    # Data validation
    "python-dotenv>=1.0.0", # Environment variables
    "tenacity>=9.1.2",     # Retry logic
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",       # Testing framework
    "pytest-cov>=4.1.0",   # Coverage reports
]
```

**Install dependencies:**
```bash
uv sync --extra dev
```

**What happens:**
- `uv` creates a virtual environment (`.venv/`) automatically
- Installs all dependencies with compatible versions
- Creates `uv.lock` file for reproducibility
- No need to manually activate virtual environment

**Key Benefits:**
- ✅ Reproducible: `uv.lock` ensures same versions everywhere
- ✅ Fast: 10-100x faster than pip
- ✅ Automatic: Creates venv, resolves conflicts, manages versions

---

### Step 3: Environment Variables with `.env`

**Why it matters:** Never hardcode API keys or secrets in your code. Environment variables keep sensitive data secure and make your code deployable across different environments.

**Create `.env` file:**
```env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

**Create `.env.example` template:**
```env
OPENAI_API_KEY=your_api_key_here
```

**Add to `.gitignore`:**
```
.env
```

**Load in your code (`src/config.py`):**
```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_openai_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY not found in environment!")
    return key
```

**Why this approach:**
- ✅ Security: API keys never appear in code or version control
- ✅ Flexibility: Different keys for dev/staging/production
- ✅ Team-friendly: `.env.example` shows what's needed without exposing secrets

---

### Step 4: Project Structure - Modules and Packages

**Why it matters:** Modular code is reusable, testable, and maintainable. Each module should have a single responsibility.

**Example structure:**

```
src/
├── __init__.py
├── config.py      # Configuration and environment setup
├── schemas.py      # Pydantic models for data validation
├── prompts.py     # Prompt engineering templates
├── analyzer.py     # Core business logic
└── utils.py       # Utility functions
```

**Example module (`src/config.py`):**
```python
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_openai_api_key() -> str:
    """Get OpenAI API key from environment."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY not found!")
    return key

def setup_logger(name: str, log_file: str = "logs/app.log") -> logging.Logger:
    """Setup logger with console and file handlers."""
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Console handler (INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    
    # File handler (DEBUG and above)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
```

**Key Principles:**
- ✅ Single Responsibility: Each module does one thing well
- ✅ Clear Imports: Use absolute imports (`from src.config import ...`)
- ✅ Reusability: Functions can be used across modules

---

### Step 5: Type Safety with Pydantic

**Why it matters:** Pydantic validates data at runtime, catches errors early, and provides clear type hints. It's essential for structured outputs from AI APIs.

**Example (`src/schemas.py`):**
```python
from pydantic import BaseModel, Field

class SentimentResult(BaseModel):
    sentiment: str = Field(
        description="The sentiment: 'Positive', 'Negative' or 'Neutral'"
    )
    score: float = Field(
        description="Confidence score between 0.0 and 1.0",
        ge=0.0,  # Greater than or equal to 0.0
        le=1.0   # Less than or equal to 1.0
    )
```

**Benefits:**
- ✅ Validation: Automatically validates data types and constraints
- ✅ Documentation: Field descriptions help AI understand expected output
- ✅ Type Safety: IDE autocomplete and type checking
- ✅ Error Messages: Clear errors when validation fails

---

### Step 6: Prompt Engineering

**Why it matters:** Well-crafted prompts are the difference between good and great AI outputs. System prompts define behavior, user prompts provide context.

**Example (`src/prompts.py`):**
```python
# System prompt defines the AI's role and behavior
SENTIMENT_SYSTEM_PROMPT = """You are an expert sentiment analyst.
Analyze text and provide accurate sentiment classifications with confidence scores.
Always respond with valid JSON matching the required schema."""

# User prompt provides the specific task
def get_sentiment_prompt(text: str) -> str:
    return f"""Analyze the sentiment of the following text:

Text: {text}

Provide a sentiment analysis with a confidence score."""
```

**Best Practices:**
- ✅ Clear Instructions: Be specific about what you want
- ✅ Examples: Include examples for complex tasks
- ✅ Constraints: Specify format requirements (JSON, structure)
- ✅ Token Awareness: Keep prompts concise to reduce costs

---

### Step 7: OpenAI API Integration

**Why it matters:** The modern `responses.parse()` API provides structured outputs, better error handling, and cleaner code than the older chat completions API.

**Example (`src/analyzer.py`):**
```python
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from src.config import get_openai_api_key, setup_logger
from src.schemas import SentimentResult
from src.prompts import SENTIMENT_SYSTEM_PROMPT, get_sentiment_prompt

client = OpenAI(api_key=get_openai_api_key())
logger = setup_logger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def analyze_sentiment(text: str) -> SentimentResult:
    logger.info("Analyzing sentiment...")
    try:
        response = client.responses.parse(
            model="gpt-4o-mini",
            instructions=SENTIMENT_SYSTEM_PROMPT,  # System prompt
            input=get_sentiment_prompt(text),       # User prompt
            text_format=SentimentResult,           # Pydantic model
            timeout=30.0
        )
        
        logger.info("Sentiment analysis completed successfully!")
        # Parse JSON string into Pydantic object
        return SentimentResult.model_validate_json(response.output_text)
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}", exc_info=True)
        raise
```

**Key Features:**
- ✅ `instructions`: System prompt (defines AI behavior)
- ✅ `input`: User prompt (the actual task)
- ✅ `text_format`: Pydantic model for structured output
- ✅ `timeout`: Prevents hanging requests
- ✅ Retry logic: Handles transient failures automatically

**Why `responses.parse()` over `chat.completions.parse()`:**
- Simpler API: Single `input` string instead of message arrays
- Better for structured outputs: Direct Pydantic model support
- Cleaner code: Less boilerplate

---

### Step 8: Error Handling and Retries

**Why it matters:** API calls can fail due to network issues, rate limits, or temporary service problems. Retry logic makes your application resilient.

**Using Tenacity for Retries:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),  # Try up to 3 times
    wait=wait_exponential(
        multiplier=1,    # Base wait time
        min=2,          # Minimum 2 seconds
        max=10          # Maximum 10 seconds
    )
)
def api_call():
    # Your API call here
    pass
```

**What happens:**
1. First attempt fails → Wait 2 seconds → Retry
2. Second attempt fails → Wait 4 seconds → Retry
3. Third attempt fails → Raise exception

**Benefits:**
- ✅ Automatic retries for transient failures
- ✅ Exponential backoff prevents overwhelming the API
- ✅ Configurable retry strategy

---

### Step 9: Logging

**Why it matters:** Logging helps you debug issues, monitor application behavior, and understand what happened in production. Never use `print()` in production code.

**Setup (`src/config.py`):**
```python
def setup_logger(name: str, log_file: str = "logs/app.log") -> logging.Logger:
    """Setup logger with console and file handlers."""
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Prevent duplicates
    
    logger.setLevel(logging.DEBUG)
    
    # Console: INFO and above (user feedback)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    
    # File: DEBUG and above (detailed logs)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
```

**Usage:**
```python
logger = setup_logger(__name__)

logger.debug("Detailed diagnostic info")      # Only in file
logger.info("Normal operation")              # Console + file
logger.warning("Something unusual")          # Console + file
logger.error("Error occurred", exc_info=True) # Console + file with stack trace
```

**Log Levels:**
- `DEBUG`: Detailed diagnostic information (development only)
- `INFO`: General informational messages (normal operation)
- `WARNING`: Something unexpected but recoverable
- `ERROR`: Serious problem, operation may continue
- `CRITICAL`: Serious error, operation may not continue

---

### Step 10: Testing

**Why it matters:** Tests ensure your code works correctly, catch bugs early, and give you confidence when making changes.

**Example Test (`tests/test_analyzer.py`):**
```python
import pytest
from unittest.mock import Mock, patch
from src.analyzer import analyze_sentiment
from src.schemas import SentimentResult

@patch("src.analyzer.client.responses.parse")
def test_analyze_sentiment_success(mock_parse):
    # Arrange: Create fake response
    fake_result = SentimentResult(sentiment="positive", score=0.95)
    mock_response = Mock()
    
    # Mock the API response (returns JSON string)
    mock_response.output_text = fake_result.model_dump_json()
    mock_parse.return_value = mock_response
    
    # Act: Call function
    result = analyze_sentiment("I love this!")
    
    # Assert: Verify result
    assert result.sentiment == "positive"
    assert result.score == 0.95
    mock_parse.assert_called_once()
```

**Running Tests:**
```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html
```

**Testing Best Practices:**
- ✅ Test happy path (normal operation)
- ✅ Test error cases (invalid input, API failures)
- ✅ Mock external dependencies (API calls, file system)
- ✅ Use descriptive test names
- ✅ Follow AAA pattern: Arrange, Act, Assert

---

### Step 11: CLI Interface

**Why it matters:** A good CLI makes your tool user-friendly and professional. `argparse` provides a standard way to build command-line interfaces.

**Example (`main.py`):**
```python
import argparse
from src.analyzer import analyze_sentiment
from src.utils import read_text_file, validate_text
from src.config import setup_logger

def main():
    setup_logger(__name__)
    
    parser = argparse.ArgumentParser(description="AI Text Analyzer CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze text")
    analyze_parser.add_argument("--file", type=str, help="Path to text file")
    analyze_parser.add_argument("--text", type=str, help="Text to analyze")
    analyze_parser.add_argument(
        "--type",
        choices=["sentiment", "summary", "topics"],
        default="sentiment",
        help="Analysis type"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.error("Please provide a command. Use 'analyze' to analyze text.")
    
    if args.command == "analyze":
        # Get text from file or direct input
        if args.file:
            text = read_text_file(args.file)
        elif args.text:
            text = args.text
        else:
            parser.error("Either --file or --text must be provided!")
        
        validate_text(text)
        
        # Run analysis
        if args.type == "sentiment":
            result = analyze_sentiment(text)
            print(f"Sentiment: {result.sentiment} (Score: {result.score})")

if __name__ == "__main__":
    main()
```

---

## Project Structure Explained

```
ai_text_analyzer/
├── src/                    # Source code package
│   ├── __init__.py        # Package initialization
│   ├── config.py          # Configuration and logging setup
│   ├── schemas.py          # Pydantic models for data validation
│   ├── prompts.py          # Prompt engineering templates
│   ├── analyzer.py         # Core AI analysis logic
│   └── utils.py           # Utility functions
├── tests/                  # Test package
│   ├── __init__.py
│   └── test_analyzer.py   # Unit tests
├── data/                   # Sample data files
├── logs/                   # Log files (auto-created)
├── .env                    # Environment variables (gitignored)
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── README.md               # This file
└── main.py                 # CLI entry point
```

---

## Key Concepts Deep Dive

### 1. Virtual Environments

**What:** Isolated Python environments for each project.

**Why:** Prevents dependency conflicts between projects.

**How:**
```bash
# uv automatically creates .venv/
uv sync

# Or manually
uv venv
uv pip install -e .
```

### 2. Dependency Management

**What:** Managing external packages your project needs.

**Why:** Ensures reproducible builds and version control.

**Tools:**
- `pyproject.toml`: Declares dependencies
- `uv.lock`: Locks exact versions
- `uv sync`: Installs dependencies

### 3. Type Hints and Pydantic

**What:** Type annotations and runtime validation.

**Why:** Catches errors early, improves IDE support, documents code.

**Example:**
```python
def process_text(text: str) -> SentimentResult:
    # Type hints: text is str, returns SentimentResult
    # Pydantic validates the return value
    pass
```

### 4. Error Handling

**What:** Gracefully handling failures.

**Why:** Makes applications resilient and user-friendly.

**Patterns:**
- Try-except blocks
- Retry logic (tenacity)
- Proper error messages
- Logging errors

### 5. Testing

**What:** Automated code verification.

**Why:** Catches bugs, enables refactoring, documents behavior.

**Types:**
- Unit tests: Test individual functions
- Integration tests: Test component interactions
- Mocking: Replace external dependencies

---

## Usage Examples

### Analyze Text Directly

```bash
python main.py analyze --text "I'm feeling great today!"
```

### Analyze from File

```bash
python main.py analyze --file data/sample.txt --type sentiment
```

### Different Analysis Types

```bash
# Sentiment analysis (default)
python main.py analyze --text "This product is amazing!"

# Summary
python main.py analyze --text "Long article text..." --type summary

# Topics
python main.py analyze --text "Article about AI and Python" --type topics
```

---

## Testing

Run the test suite:

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html

# Run specific test
uv run pytest tests/test_analyzer.py::test_analyze_sentiment_success -v
```

---

## Best Practices Summary

### ✅ DO:

1. **Use virtual environments** - Isolate dependencies
2. **Use `pyproject.toml`** - Modern dependency management
3. **Store secrets in `.env`** - Never commit API keys
4. **Use logging, not `print()`** - Professional debugging
5. **Write tests** - Catch bugs early
6. **Use type hints** - Document and validate code
7. **Handle errors gracefully** - Retry logic, clear messages
8. **Modular code structure** - Single responsibility
9. **Use Pydantic** - Validate structured outputs
10. **Document your code** - Help others (and future you)

### ❌ DON'T:

1. **Don't hardcode API keys** - Use environment variables
2. **Don't use `print()` in production** - Use logging
3. **Don't skip error handling** - Always handle exceptions
4. **Don't ignore tests** - Write tests as you code
5. **Don't commit `.env` files** - Add to `.gitignore`
6. **Don't mix concerns** - Keep modules focused
7. **Don't ignore type hints** - They catch bugs
8. **Don't skip documentation** - Future you will thank you

---

## Next Steps

Now that you understand the fundamentals:

1. **Extend the project:** Add more analysis types
2. **Improve prompts:** Experiment with different prompt strategies
3. **Add features:** Batch processing, file output, etc.
4. **Deploy:** Learn about deployment and production considerations
5. **Optimize:** Token usage, caching, performance

---

## Resources

- [OpenAI Python SDK Documentation](https://github.com/openai/openai-python)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [pytest Documentation](https://docs.pytest.org/)
- [Python Logging Guide](https://docs.python.org/3/library/logging.html)

---

## License

This project is for educational purposes. Feel free to use it as a template for your own AI projects!

---

**Remember:** Building great AI projects is about combining solid software engineering fundamentals with AI-specific best practices. Master the basics, and you'll be able to build anything! 🚀

