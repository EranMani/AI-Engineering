SENTIMENT_SYSTEM_PROMPT = """You are an expert sentiment analyst.
Analyze text and provide accurate sentiment classifications with confidence scores.
Always respond with valid JSON matching the required schema."""

SUMMARY_SYSTEM_PROMPT = """You are an expert at summarizing text and extracting key points.
Provide concise, accurate summaries with clear bullet points.
Always respond with valid JSON matching the required schema."""

TOPICS_SYSTEM_PROMPT = """You are an expert at identifying topics and themes in text.
Identify main topics and determine the primary topic accurately.
Always respond with valid JSON matching the required schema."""

def get_sentiment_prompt(text: str) -> str:
    return f"""Analyze the sentiment of the following text
            Text: {text}

            Provide a sentiment analysis with a confidence score.
            """

def get_summary_prompt(text: str) -> str:
    return f"""
            Analyze the following text

            Text: {text}

            Provide a concise summary while extracting key points.
            """

def get_topics_prompt(text: str) -> str:
    return f"""
            Analyze the following text

            Text: {text}

            Identify and provide the main topics and find the most prominent topic
            """