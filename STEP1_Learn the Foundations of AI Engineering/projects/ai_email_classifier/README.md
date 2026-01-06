# AI Email Classifier - Complete Foundation Project

A comprehensive AI-powered email classification CLI tool that demonstrates all foundational AI engineering concepts. This project serves as a complete template for building production-ready AI applications with clean code structure, proper error handling, logging, testing, and modern dependency management.

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Project Structure Explained](#project-structure-explained)
4. [File-by-File Explanation](#file-by-file-explanation)
5. [Usage Examples](#usage-examples)
6. [Testing](#testing)
7. [Best Practices](#best-practices)

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

### Features

The AI Email Classifier can analyze emails in three ways:

1. **Priority Classification** - Classifies emails as High, Medium, or Low priority
2. **Category Classification** - Categorizes emails as Work, Personal, Spam, Newsletter, Support, or Other
3. **Information Extraction** - Extracts sender intent, action requirements, urgency indicators, and key phrases

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd ai_email_classifier
   ```

2. **Create virtual environment and install dependencies:**
   ```bash
   uv venv
   uv sync --extra dev
   ```

3. **Set up environment variables:**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```
   
   Or manually create a `.env` file:
   ```env
   OPENAI_API_KEY=sk-proj-your-actual-api-key-here
   ```

4. **Run the application:**
   ```bash
   python main.py classify --text "This is an urgent work email!" --type priority
   ```

---

## Project Structure Explained

```
ai_email_classifier/
├── src/                    # Source code package
│   ├── __init__.py        # Package initialization
│   ├── config.py          # Configuration and logging setup
│   ├── schemas.py          # Pydantic models for data validation
│   ├── prompts.py          # Prompt engineering templates
│   ├── classifier.py       # Core AI classification logic
│   └── utils.py           # Utility functions
├── tests/                  # Test package
│   ├── __init__.py
│   └── test_classifier.py # Unit tests with mocking
├── data/                   # Sample email files
│   ├── urgent_work_email.txt
│   ├── newsletter_email.txt
│   ├── personal_email.txt
│   └── support_request.txt
├── logs/                   # Log files (auto-created)
├── .venv/                  # Virtual environment (auto-created)
├── .env                    # Environment variables (gitignored)
├── .env.example            # Template for .env
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file (auto-generated)
├── README.md               # This file
└── main.py                 # CLI entry point
```

---

## File-by-File Explanation

### Core Application Files

#### `main.py`
The command-line interface entry point. Uses `argparse` to handle user commands and arguments.

**Key Features:**
- Parses command-line arguments (`--file`, `--text`, `--type`)
- Validates email content before processing
- Routes to appropriate classification function based on `--type`
- Formats and displays results

**Usage:**
```bash
python main.py classify --file data/urgent_work_email.txt --type priority
python main.py classify --text "Email content here" --type category
```

#### `src/config.py`
Handles configuration and logging setup.

**Functions:**
- `get_openai_api_key()` - Retrieves OpenAI API key from environment variables
- `setup_logger()` - Configures dual logging (console + file)

**Key Features:**
- Loads environment variables using `python-dotenv`
- Creates logs directory automatically
- Console handler shows INFO+ messages
- File handler logs DEBUG+ messages with timestamps

#### `src/schemas.py`
Defines Pydantic models for structured AI outputs.

**Models:**
- `PriorityResult` - Contains `priority` (High/Medium/Low) and `confidence` (0.0-1.0)
- `CategoryResult` - Contains `category` (Work/Personal/Spam/etc.) and `confidence` (0.0-1.0)
- `EmailInfoResult` - Contains `sender_intent`, `action_required` (bool), `urgency_indicators` (list), `key_phrases` (list)

**Why Pydantic:**
- Validates data types and constraints at runtime
- Provides clear error messages
- Field descriptions help AI understand expected output format
- Type hints improve IDE support

#### `src/prompts.py`
Contains prompt engineering templates for each classification type.

**System Prompts:**
- `PRIORITY_SYSTEM_PROMPT` - Defines AI role as priority analyst
- `CATEGORY_SYSTEM_PROMPT` - Defines AI role as email categorizer
- `INFO_SYSTEM_PROMPT` - Defines AI role as information extractor

**User Prompt Functions:**
- `get_priority_prompt(email_content)` - Generates prompt for priority classification
- `get_category_prompt(email_content)` - Generates prompt for category classification
- `get_info_prompt(email_content)` - Generates prompt for information extraction

**Best Practices:**
- System prompts define the AI's role and behavior
- User prompts provide specific email content
- Clear instructions ensure consistent output format

#### `src/classifier.py`
Core classification logic with OpenAI API integration.

**Functions:**
- `classify_priority(email_content)` - Classifies email priority
- `classify_category(email_content)` - Classifies email category
- `extract_email_info(email_content)` - Extracts key information

**Key Features:**
- Uses `@retry` decorator for automatic retries (3 attempts, exponential backoff)
- Logs all operations for debugging
- Uses `gpt-4o-mini` model for cost efficiency
- 30-second timeout to prevent hanging requests
- Proper error handling with exception logging

**Retry Logic:**
- Attempts: 3 tries maximum
- Backoff: Exponential (2s, 4s, 8s)
- Handles transient API failures automatically

#### `src/utils.py`
Utility functions for file operations and validation.

**Functions:**
- `read_email_file(file_path)` - Reads email content from file
- `validate_email_content(content)` - Validates email content

**Validation Rules:**
- Content cannot be empty
- Minimum length: 10 characters
- Maximum length: 100,000 characters (100KB)

### Configuration Files

#### `pyproject.toml`
Modern Python project configuration file.

**Sections:**
- `[project]` - Project metadata and dependencies
- `[project.optional-dependencies]` - Development dependencies (pytest, pytest-cov)

**Dependencies:**
- `openai>=2.14.0` - OpenAI API client
- `pydantic>=2.12.5` - Data validation
- `python-dotenv>=1.0.0` - Environment variable management
- `tenacity>=9.1.2` - Retry logic

#### `.env.example`
Template for environment variables. Copy to `.env` and add your actual API key.

#### `.gitignore`
Excludes sensitive files and generated content from version control:
- `.env` (API keys)
- `__pycache__/` (Python cache)
- `.venv/` (Virtual environment)
- `logs/` (Log files)
- `.pytest_cache/` (Test cache)

### Test Files

#### `tests/test_classifier.py`
Unit tests for classification functions using mocking.

**Test Cases:**
- `test_classify_priority_success` - Tests successful priority classification
- `test_classify_category_success` - Tests successful category classification
- `test_extract_email_info_success` - Tests successful info extraction
- `test_classify_priority_api_failure` - Tests error handling

**Testing Approach:**
- Mocks OpenAI API calls to avoid real API usage during tests
- Tests both success and failure scenarios
- Follows AAA pattern: Arrange, Act, Assert

### Sample Data

#### `data/urgent_work_email.txt`
Sample high-priority work email for testing.

#### `data/newsletter_email.txt`
Sample newsletter/spam email for testing.

#### `data/personal_email.txt`
Sample personal email for testing.

#### `data/support_request.txt`
Sample support ticket email for testing.

---

## Usage Examples

### Priority Classification

Classify an email's priority level:

```bash
# Using direct text input
python main.py classify --text "URGENT: Project deadline tomorrow at 5 PM. Please review ASAP!" --type priority

# Using a file
python main.py classify --file data/urgent_work_email.txt --type priority
```

**Expected Output:**
```
Priority: High (Confidence: 0.95)
```

### Category Classification

Categorize an email:

```bash
# Classify a work email
python main.py classify --text "Meeting tomorrow at 2pm in conference room" --type category

# Classify a newsletter
python main.py classify --file data/newsletter_email.txt --type category
```

**Expected Output:**
```
Category: Work (Confidence: 0.92)
```

### Information Extraction

Extract detailed information from an email:

```bash
# Extract info from support request
python main.py classify --file data/support_request.txt --type info

# Extract info from direct text
python main.py classify --text "Can we schedule a meeting tomorrow? It's urgent and I need your feedback on the proposal." --type info
```

**Expected Output:**
```
Sender Intent: Request for meeting and feedback
Action Required: True
Urgency Indicators: urgent, ASAP
Key Phrases: meeting, tomorrow, feedback, proposal
```

### Complete Example Workflow

```bash
# 1. Classify priority
python main.py classify --file data/urgent_work_email.txt --type priority

# 2. Classify category
python main.py classify --file data/urgent_work_email.txt --type category

# 3. Extract information
python main.py classify --file data/urgent_work_email.txt --type info
```

---

## Testing

### Running Tests

Run all tests:
```bash
uv run pytest tests/ -v
```

Run with coverage report:
```bash
uv run pytest tests/ --cov=src --cov-report=html
```

Run a specific test:
```bash
uv run pytest tests/test_classifier.py::test_classify_priority_success -v
```

### Test Structure

Tests use mocking to avoid real API calls:
- `@patch` decorator mocks the OpenAI API
- Tests verify function behavior without network calls
- Both success and failure scenarios are tested

### Example Test Output

```
tests/test_classifier.py::test_classify_priority_success PASSED
tests/test_classifier.py::test_classify_category_success PASSED
tests/test_classifier.py::test_extract_email_info_success PASSED
tests/test_classifier.py::test_classify_priority_api_failure PASSED

========== 4 passed in 0.15s ==========
```

---

## Best Practices

### ✅ DO:

1. **Use virtual environments** - Isolate dependencies per project
2. **Use `pyproject.toml`** - Modern dependency management
3. **Store secrets in `.env`** - Never commit API keys
4. **Use logging, not `print()`** - Professional debugging
5. **Write tests** - Catch bugs early
6. **Use type hints** - Document and validate code
7. **Handle errors gracefully** - Retry logic, clear messages
8. **Modular code structure** - Single responsibility principle
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

## Key Concepts Demonstrated

### 1. Virtual Environments
Isolated Python environments prevent dependency conflicts. `uv` automatically creates and manages `.venv/`.

### 2. Dependency Management
`pyproject.toml` declares dependencies, `uv.lock` locks exact versions for reproducibility.

### 3. Type Safety with Pydantic
Runtime validation ensures data integrity and provides clear error messages.

### 4. Error Handling
Retry logic with exponential backoff handles transient API failures gracefully.

### 5. Logging
Dual logging (console + file) provides visibility into application behavior.

### 6. Testing
Unit tests with mocking verify functionality without external dependencies.

### 7. OpenAI API Integration
Modern `responses.parse()` API provides structured outputs with Pydantic models.

### 8. Prompt Engineering
Well-crafted prompts ensure consistent, accurate AI outputs.

---

## Troubleshooting

### Common Issues

**Import errors:**
- Ensure you're in the project root directory
- Check that `src/__init__.py` exists
- Use `uv run python main.py` if virtual environment issues occur

**API key not found:**
- Verify `.env` file exists in project root
- Check `OPENAI_API_KEY` is set correctly
- Ensure `python-dotenv` is installed

**Module not found:**
- Verify all `__init__.py` files exist
- Check import paths use `from src.module import ...`

**Tests fail:**
- Ensure you're mocking the API correctly
- Check that test imports match module structure

---

## Next Steps

1. **Experiment with prompts** - Try different prompt styles and see how they affect results
2. **Add more features** - Batch processing, JSON output, email filtering
3. **Improve error handling** - Add more specific error types
4. **Extend categories** - Add more email categories (Promotional, Social, etc.)
5. **Add caching** - Cache results to reduce API calls and costs
6. **Create a web interface** - Build a simple web UI using Flask or FastAPI

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

