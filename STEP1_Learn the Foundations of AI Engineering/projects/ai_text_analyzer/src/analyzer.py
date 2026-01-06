from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from src.prompts import get_sentiment_prompt, get_summary_prompt, get_topics_prompt, SENTIMENT_SYSTEM_PROMPT, SUMMARY_SYSTEM_PROMPT, TOPICS_SYSTEM_PROMPT
from src.config import get_openai_api_key, setup_logger
from src.schemas import SentimentResult, SummaryResult, TopicResult


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
            model="gpt-5-mini",
            instructions=SENTIMENT_SYSTEM_PROMPT,
            input=get_sentiment_prompt(text),
            text_format=SentimentResult,
            timeout=30.0
        )

        logger.info("Sentiment analysis completed successfully!")
        return SentimentResult.model_validate_json(response.output_text)
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}", exc_info=True)
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def analyze_summary(text: str) -> SummaryResult:
    logger.info("Generating summary...")
    try:
        response = client.responses.parse(
            model="gpt-5-mini",
            instructions=SUMMARY_SYSTEM_PROMPT,
            input=get_summary_prompt(text),
            text_format=SummaryResult,
            timeout=30.0
        )

        logger.info("Summary generation completed successfully!")
        return SummaryResult.model_validate_json(response.output_text)
    except Exception as e:
        logger.error(f"Summary generation failed: {e}", exc_info=True)
        raise

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def analyze_topics(text: str) -> TopicResult:
    logger.info("Extracting info...")
    try:
        response = client.responses.parse(
            model="gpt-5-mini",
            instructions=TOPICS_SYSTEM_PROMPT,
            input=get_topics_prompt(text),
            text_format=TopicResult,
            timeout=30.0
        )
        logger.info(f"Topic extraction completed successfully!")
        return TopicResult.model_validate_json(response.output_text)
    except Exception as e:
        logger.error(f"Topic extraction failed: {e}", exc_info=True)
        raise