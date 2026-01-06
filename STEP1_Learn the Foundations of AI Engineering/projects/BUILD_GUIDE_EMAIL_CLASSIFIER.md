# Step-by-Step Build Guide: AI Email Classifier

This guide walks you through building the AI Email Classifier project step by step. Follow each step in order, and refer to the `ai_text_analyzer` project as a reference when needed.

---

## Step 1: Setup Project Structure

**Goal:** Create the directory structure and package files.

### Actions:

1. **Navigate to the projects directory:**
   ```bash
   cd "STEP1_Learn the Foundations of AI Engineering/projects"
   ```

2. **Create the project directory:**
   ```bash
   mkdir ai_email_classifier
   cd ai_email_classifier
   ```

3. **Create all subdirectories:**
   ```bash
   mkdir src
   mkdir tests
   mkdir data
   mkdir logs
   ```

4. **Create `__init__.py` files to make directories Python packages:**
   
   **Create `src/__init__.py`:**
   ```python
   # src/__init__.py
   # Package initialization - can be empty or export main classes
   ```
   
   **Create `tests/__init__.py`:**
   ```python
   # tests/__init__.py
   # Test package initialization
   ```

### Verification:
- You should have: `src/`, `tests/`, `data/`, `logs/` directories
- Both `src/` and `tests/` should have `__init__.py` files

---

## Step 2: Setup Dependencies

**Goal:** Create `pyproject.toml` with project metadata and dependencies.

### Actions:

1. **Create `pyproject.toml` in the project root:**
   ```toml
   [project]
   name = "ai-email-classifier"
   version = "0.1.0"
   description = "AI-powered email classification CLI tool"
   readme = "README.md"
   requires-python = ">=3.10"
   dependencies = [
       "openai>=2.14.0",
       "pydantic>=2.12.5",
       "python-dotenv>=1.0.0",
       "tenacity>=9.1.2",
   ]
   
   [project.optional-dependencies]
   dev = [
       "pytest>=8.0.0",
       "pytest-cov>=4.1.0",
   ]
   ```

2. **Install dependencies:**
   ```bash
   uv sync --extra dev
   ```
   This will:
   - Create a virtual environment (`.venv/`)
   - Install all dependencies
   - Generate `uv.lock` file

### Verification:
- `pyproject.toml` exists with correct content
- `.venv/` directory created
- `uv.lock` file generated

---

## Step 3: Implement Configuration Module

**Goal:** Create `src/config.py` with API key management and logging setup.

### Actions:

1. **Create `src/config.py`:**
   ```python
   import os
   import logging
   from pathlib import Path
   from dotenv import load_dotenv
   
   # Load environment variables from .env file
   load_dotenv()
   
   def get_openai_api_key() -> str:
       """Get OpenAI API key from environment."""
       key = os.getenv("OPENAI_API_KEY")
       if not key:
           raise ValueError("OPENAI_API_KEY not found in environment!")
       return key
   
   def setup_logger(name: str, log_file: str = "logs/app.log") -> logging.Logger:
       """Setup logger with console and file handlers."""
       # Create logs directory if it doesn't exist
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
       file_format = logging.Formatter(
           '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
       )
       file_handler.setFormatter(file_format)
       
       logger.addHandler(console_handler)
       logger.addHandler(file_handler)
       
       return logger
   ```

### Key Points:
- `load_dotenv()` loads variables from `.env` file
- `get_openai_api_key()` raises error if key is missing
- `setup_logger()` creates dual handlers (console + file)
- Logs directory is created automatically

### Verification:
- File exists at `src/config.py`
- No syntax errors (you can test with `python -m py_compile src/config.py`)

---

## Step 4: Implement Schemas Module

**Goal:** Create Pydantic models for structured outputs.

### Actions:

1. **Create `src/schemas.py`:**
   ```python
   from pydantic import BaseModel, Field
   
   class PriorityResult(BaseModel):
       """Result of priority classification."""
       priority: str = Field(
           description="Email priority: 'High', 'Medium', or 'Low'"
       )
       confidence: float = Field(
           description="Confidence score between 0.0 and 1.0",
           ge=0.0,
           le=1.0
       )
   
   class CategoryResult(BaseModel):
       """Result of category classification."""
       category: str = Field(
           description="Email category: 'Work', 'Personal', 'Spam', 'Newsletter', 'Support', or 'Other'"
       )
       confidence: float = Field(
           description="Confidence score between 0.0 and 1.0",
           ge=0.0,
           le=1.0
       )
   
   class EmailInfoResult(BaseModel):
       """Extracted information from email."""
       sender_intent: str = Field(
           description="The main intent or purpose of the email sender"
       )
       action_required: bool = Field(
           description="Whether the email requires any action from the recipient"
       )
       urgency_indicators: list[str] = Field(
           description="List of phrases or words that indicate urgency",
           default_factory=list
       )
       key_phrases: list[str] = Field(
           description="Important phrases or keywords extracted from the email",
           default_factory=list
       )
   ```

### Key Points:
- Each model uses `Field()` with descriptions (helps AI understand expected output)
- `confidence` scores are constrained between 0.0 and 1.0
- Lists use `default_factory=list` to avoid mutable default arguments

### Verification:
- File exists at `src/schemas.py`
- No syntax errors

---

## Step 5: Implement Prompts Module

**Goal:** Create prompt templates for each classification type.

### Actions:

1. **Create `src/prompts.py`:**
   ```python
   PRIORITY_SYSTEM_PROMPT = """You are an expert at analyzing email priority.
   Classify emails as High, Medium, or Low priority based on urgency, importance, and action required.
   Consider factors like deadlines, sender importance, and content urgency.
   Always respond with valid JSON matching the required schema."""
   
   CATEGORY_SYSTEM_PROMPT = """You are an expert at categorizing emails.
   Classify emails into categories: Work, Personal, Spam, Newsletter, Support, or Other.
   Consider the sender, content, and purpose of the email.
   Always respond with valid JSON matching the required schema."""
   
   INFO_SYSTEM_PROMPT = """You are an expert at extracting key information from emails.
   Identify the sender's intent, whether action is required, urgency indicators, and key phrases.
   Be precise and extract only relevant information.
   Always respond with valid JSON matching the required schema."""
   
   def get_priority_prompt(email_content: str) -> str:
       """Generate prompt for priority classification."""
       return f"""Analyze the priority of the following email:
   
   Email Content:
   {email_content}
   
   Classify the priority as High, Medium, or Low and provide a confidence score."""
   
   def get_category_prompt(email_content: str) -> str:
       """Generate prompt for category classification."""
       return f"""Categorize the following email:
   
   Email Content:
   {email_content}
   
   Classify the email into one of these categories: Work, Personal, Spam, Newsletter, Support, or Other.
   Provide a confidence score."""
   
   def get_info_prompt(email_content: str) -> str:
       """Generate prompt for information extraction."""
       return f"""Extract key information from the following email:
   
   Email Content:
   {email_content}
   
   Identify:
   - The sender's main intent or purpose
   - Whether any action is required from the recipient
   - Any urgency indicators (phrases, words, or patterns)
   - Key phrases or important keywords"""
   ```

### Key Points:
- System prompts define the AI's role and behavior
- User prompts provide the specific email content
- Prompts are clear and specific about expected output

### Verification:
- File exists at `src/prompts.py`
- All three system prompts and three prompt functions are defined

---

## Step 6: Implement Utils Module

**Goal:** Create utility functions for file reading and validation.

### Actions:

1. **Create `src/utils.py`:**
   ```python
   from pathlib import Path
   
   def read_email_file(file_path: str) -> str:
       """Read email content from a file."""
       path = Path(file_path)
       if not path.exists():
           raise FileNotFoundError(f"Email file not found: {file_path}")
       
       content = path.read_text(encoding="utf-8")
       if not content.strip():
           raise ValueError(f"Email file is empty: {file_path}")
       
       return content
   
   def validate_email_content(content: str) -> None:
       """Validate email content."""
       if not content or not content.strip():
           raise ValueError("Email content cannot be empty!")
       
       if len(content) > 100000:  # 100KB limit
           raise ValueError("Email content is too long (max 100KB)!")
       
       if len(content.strip()) < 10:
           raise ValueError("Email content is too short (minimum 10 characters)!")
   ```

### Key Points:
- Uses `Path` for cross-platform file handling
- Validates file existence and content
- Sets reasonable limits (min 10 chars, max 100KB)

### Verification:
- File exists at `src/utils.py`
- Functions handle edge cases (missing file, empty content)

---

## Step 7: Implement Classifier Module

**Goal:** Create the core classification functions with retry logic.

### Actions:

1. **Create `src/classifier.py`:**
   ```python
   from openai import OpenAI
   from tenacity import retry, stop_after_attempt, wait_exponential
   from src.config import get_openai_api_key, setup_logger
   from src.schemas import PriorityResult, CategoryResult, EmailInfoResult
   from src.prompts import (
       PRIORITY_SYSTEM_PROMPT,
       CATEGORY_SYSTEM_PROMPT,
       INFO_SYSTEM_PROMPT,
       get_priority_prompt,
       get_category_prompt,
       get_info_prompt
   )
   
   client = OpenAI(api_key=get_openai_api_key())
   logger = setup_logger(__name__)
   
   @retry(
       stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=2, max=10)
   )
   def classify_priority(email_content: str) -> PriorityResult:
       """Classify email priority."""
       logger.info("Classifying email priority...")
       try:
           response = client.responses.parse(
               model="gpt-4o-mini",
               instructions=PRIORITY_SYSTEM_PROMPT,
               input=get_priority_prompt(email_content),
               text_format=PriorityResult,
               timeout=30.0
           )
           
           logger.info("Priority classification completed successfully!")
           return PriorityResult.model_validate_json(response.output_text)
       except Exception as e:
           logger.error(f"Priority classification failed: {e}", exc_info=True)
           raise
   
   @retry(
       stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=2, max=10)
   )
   def classify_category(email_content: str) -> CategoryResult:
       """Classify email category."""
       logger.info("Classifying email category...")
       try:
           response = client.responses.parse(
               model="gpt-4o-mini",
               instructions=CATEGORY_SYSTEM_PROMPT,
               input=get_category_prompt(email_content),
               text_format=CategoryResult,
               timeout=30.0
           )
           
           logger.info("Category classification completed successfully!")
           return CategoryResult.model_validate_json(response.output_text)
       except Exception as e:
           logger.error(f"Category classification failed: {e}", exc_info=True)
           raise
   
   @retry(
       stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=2, max=10)
   )
   def extract_email_info(email_content: str) -> EmailInfoResult:
       """Extract key information from email."""
       logger.info("Extracting email information...")
       try:
           response = client.responses.parse(
               model="gpt-4o-mini",
               instructions=INFO_SYSTEM_PROMPT,
               input=get_info_prompt(email_content),
               text_format=EmailInfoResult,
               timeout=30.0
           )
           
           logger.info("Email information extraction completed successfully!")
           return EmailInfoResult.model_validate_json(response.output_text)
       except Exception as e:
           logger.error(f"Email information extraction failed: {e}", exc_info=True)
           raise
   ```

### Key Points:
- Uses `@retry` decorator for automatic retries (3 attempts, exponential backoff)
- Each function follows the same pattern: log → API call → parse → return
- Error handling with logging
- Uses `gpt-4o-mini` for cost efficiency

### Verification:
- File exists at `src/classifier.py`
- All three functions are implemented
- Imports are correct

---

## Step 8: Implement CLI Interface

**Goal:** Create the command-line interface using argparse.

### Actions:

1. **Create `main.py` in the project root:**
   ```python
   import argparse
   from src.classifier import classify_priority, classify_category, extract_email_info
   from src.utils import read_email_file, validate_email_content
   from src.config import setup_logger
   
   def main():
       setup_logger(__name__)
       
       parser = argparse.ArgumentParser(
           description="AI Email Classifier CLI"
       )
       subparsers = parser.add_subparsers(
           dest="command",
           help="Available commands"
       )
       
       # Classify command
       classify_parser = subparsers.add_parser(
           "classify",
           help="Classify an email"
       )
       classify_parser.add_argument(
           "--file",
           type=str,
           help="Path to the email file"
       )
       classify_parser.add_argument(
           "--text",
           type=str,
           help="Email content as text"
       )
       classify_parser.add_argument(
           "--type",
           choices=["priority", "category", "info"],
           default="priority",
           help="Classification type (default: priority)"
       )
       
       args = parser.parse_args()
       
       if not args.command:
           parser.error("Please provide a command. Use 'classify' to classify an email.")
       
       if args.command == "classify":
           # Get email content from file or direct input
           if args.file:
               email_content = read_email_file(args.file)
           elif args.text:
               email_content = args.text
           else:
               parser.error("Either --file or --text must be provided!")
           
           validate_email_content(email_content)
           
           # Run classification based on type
           if args.type == "priority":
               result = classify_priority(email_content)
               print(f"Priority: {result.priority} (Confidence: {result.confidence:.2f})")
           elif args.type == "category":
               result = classify_category(email_content)
               print(f"Category: {result.category} (Confidence: {result.confidence:.2f})")
           elif args.type == "info":
               result = extract_email_info(email_content)
               print(f"Sender Intent: {result.sender_intent}")
               print(f"Action Required: {result.action_required}")
               print(f"Urgency Indicators: {', '.join(result.urgency_indicators) if result.urgency_indicators else 'None'}")
               print(f"Key Phrases: {', '.join(result.key_phrases) if result.key_phrases else 'None'}")
   
   if __name__ == "__main__":
       main()
   ```

### Key Points:
- Uses `argparse` for CLI
- Supports both `--file` and `--text` options
- Three classification types: priority, category, info
- Validates input before processing
- Clear output formatting

### Verification:
- File exists at `main.py`
- Can test help: `python main.py --help`
- Can test command help: `python main.py classify --help`

---

## Step 9: Write Tests

**Goal:** Create unit tests with mocking.

### Actions:

1. **Create `tests/test_classifier.py`:**
   ```python
   import pytest
   from unittest.mock import Mock, patch
   from src.classifier import classify_priority, classify_category, extract_email_info
   from src.schemas import PriorityResult, CategoryResult, EmailInfoResult
   
   @patch("src.classifier.client.responses.parse")
   def test_classify_priority_success(mock_parse):
       """Test successful priority classification."""
       # Arrange: Create fake response
       fake_result = PriorityResult(priority="High", confidence=0.95)
       mock_response = Mock()
       mock_response.output_text = fake_result.model_dump_json()
       mock_parse.return_value = mock_response
       
       # Act: Call function
       result = classify_priority("Urgent: Please review this ASAP!")
       
       # Assert: Verify result
       assert result.priority == "High"
       assert result.confidence == 0.95
       mock_parse.assert_called_once()
   
   @patch("src.classifier.client.responses.parse")
   def test_classify_category_success(mock_parse):
       """Test successful category classification."""
       # Arrange
       fake_result = CategoryResult(category="Work", confidence=0.92)
       mock_response = Mock()
       mock_response.output_text = fake_result.model_dump_json()
       mock_parse.return_value = mock_response
       
       # Act
       result = classify_category("Meeting tomorrow at 2pm")
       
       # Assert
       assert result.category == "Work"
       assert result.confidence == 0.92
       mock_parse.assert_called_once()
   
   @patch("src.classifier.client.responses.parse")
   def test_extract_email_info_success(mock_parse):
       """Test successful email info extraction."""
       # Arrange
       fake_result = EmailInfoResult(
           sender_intent="Request for meeting",
           action_required=True,
           urgency_indicators=["ASAP", "urgent"],
           key_phrases=["meeting", "tomorrow"]
       )
       mock_response = Mock()
       mock_response.output_text = fake_result.model_dump_json()
       mock_parse.return_value = mock_response
       
       # Act
       result = extract_email_info("Can we meet tomorrow? It's urgent!")
       
       # Assert
       assert result.sender_intent == "Request for meeting"
       assert result.action_required is True
       assert len(result.urgency_indicators) == 2
       assert "ASAP" in result.urgency_indicators
       mock_parse.assert_called_once()
   
   @patch("src.classifier.client.responses.parse")
   def test_classify_priority_api_failure(mock_parse):
       """Test error handling when API fails."""
       # Arrange: Mock API failure
       mock_parse.side_effect = Exception("API Error")
       
       # Act & Assert: Should raise exception
       with pytest.raises(Exception, match="API Error"):
           classify_priority("Test email")
   ```

### Key Points:
- Uses `@patch` to mock the OpenAI API
- Tests happy path (success cases)
- Tests error handling
- Follows AAA pattern: Arrange, Act, Assert

### Verification:
- File exists at `tests/test_classifier.py`
- Run tests: `uv run pytest tests/ -v`
- All tests should pass (with mocked API)

---

## Step 10: Create Sample Data

**Goal:** Create sample email files for testing.

### Actions:

1. **Create `data/urgent_work_email.txt`:**
   ```
   Subject: URGENT: Project Deadline Tomorrow
   
   Hi Team,
   
   This is urgent - we need to finalize the project proposal by tomorrow at 5 PM.
   Please review the attached document and provide your feedback ASAP.
   
   The client is waiting for our response, so this is a high priority task.
   
   Thanks,
   Manager
   ```

2. **Create `data/newsletter_email.txt`:**
   ```
   Subject: Weekly Tech Newsletter - Issue #42
   
   Hello Subscriber,
   
   Welcome to this week's tech newsletter! We've got exciting updates:
   - New AI developments
   - Python tips and tricks
   - Industry news
   
   Read more on our website.
   
   Unsubscribe | Manage Preferences
   ```

3. **Create `data/personal_email.txt`:**
   ```
   Subject: Weekend Plans?
   
   Hey,
   
   Are you free this weekend? I was thinking we could grab lunch on Saturday.
   Let me know what works for you!
   
   Cheers,
   Friend
   ```

4. **Create `data/support_request.txt`:**
   ```
   Subject: Need Help with Account Access
   
   Hello Support Team,
   
   I'm having trouble accessing my account. I've tried resetting my password
   but it's not working. Can someone please help me resolve this issue?
   
   My account email is: user@example.com
   
   Thank you,
   Customer
   ```

### Verification:
- All four files exist in `data/` directory
- Files contain realistic email content

---

## Step 11: Write README

**Goal:** Create comprehensive documentation.

### Actions:

1. **Create `README.md` in the project root:**
   
   You can model this after `ai_text_analyzer/README.md`. Include:
   - Project overview
   - Quick start guide
   - Installation instructions
   - Usage examples
   - Project structure explanation
   - Testing instructions
   - Best practices
   
   **Key sections to include:**
   ```markdown
   # AI Email Classifier
   
   A comprehensive AI-powered email classification CLI tool...
   
   ## Quick Start
   [Installation and setup]
   
   ## Usage Examples
   [Command examples]
   
   ## Project Structure
   [Directory explanation]
   
   ## Testing
   [How to run tests]
   ```

### Reference:
- Look at `ai_text_analyzer/README.md` for structure and style
- Adapt the content for email classification

---

## Step 12: Setup Environment Files

**Goal:** Create `.env.example` and `.gitignore`.

### Actions:

1. **Create `.env.example`:**
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

2. **Create `.gitignore`:**
   ```
   # Environment variables
   .env
   
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   
   # Virtual environment
   .venv/
   venv/
   ENV/
   
   # Testing
   .pytest_cache/
   .coverage
   htmlcov/
   
   # Logs
   logs/
   *.log
   
   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo
   
   # OS
   .DS_Store
   Thumbs.db
   
   # Lock file (optional - some teams commit it)
   # uv.lock
   ```

### Verification:
- `.env.example` exists
- `.gitignore` exists
- `.env` is in `.gitignore` (never commit your actual API key!)

---

## Final Steps: Testing Your Project

1. **Set up your API key:**
   ```bash
   # Create .env file (copy from .env.example)
   echo "OPENAI_API_KEY=sk-proj-your-actual-key" > .env
   ```

2. **Test the CLI:**
   ```bash
   # Test with direct text
   python main.py classify --text "This is an urgent work email!" --type priority
   
   # Test with file
   python main.py classify --file data/urgent_work_email.txt --type category
   
   # Test info extraction
   python main.py classify --file data/support_request.txt --type info
   ```

3. **Run tests:**
   ```bash
   uv run pytest tests/ -v
   ```

4. **Check logs:**
   ```bash
   # View log file
   cat logs/app.log
   ```

---

## Troubleshooting

### Common Issues:

1. **Import errors:**
   - Make sure you're in the project root
   - Check that `src/__init__.py` exists
   - Use `uv run python main.py` if virtual environment issues

2. **API key not found:**
   - Check `.env` file exists
   - Verify `OPENAI_API_KEY` is set correctly
   - Make sure `python-dotenv` is installed

3. **Module not found:**
   - Ensure all `__init__.py` files exist
   - Check import paths (use `from src.module import ...`)

4. **Tests fail:**
   - Make sure you're mocking the API correctly
   - Check that test imports match your actual module structure

---

## Next Steps After Building

1. **Experiment with prompts:** Try different prompt styles
2. **Add more features:** Batch processing, JSON output, etc.
3. **Improve error handling:** Add more specific error types
4. **Extend categories:** Add more email categories
5. **Add caching:** Cache results to reduce API calls

---

**Remember:** Take your time with each step. Understanding the code is more important than speed. Refer back to `ai_text_analyzer` whenever you need a reference!

