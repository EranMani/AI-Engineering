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
    """Classify email priority"""
    logger.info("Classifying email priority...")
    try:
        response = client.responses.parse(
            model="gpt-5-mini",
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
    """Classify email category"""
    logger.info("Classifying email category...")
    try:
        response = client.responses.parse(
            model="gpt-5-mini",
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
    """Extract key information from email"""
    logger.info("Extracting email information...")
    try:
        response = client.responses.parse(
            model="gpt-5-mini",
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