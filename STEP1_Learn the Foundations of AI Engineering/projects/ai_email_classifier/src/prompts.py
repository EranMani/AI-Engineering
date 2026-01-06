PRIORITY_SYSTEM_PROMPT = """
You are an expert at analyzing email priority.
Classify emails as High, Medium, or Low priority based on urgency, importance and action required.
Consider factors like deadlines, sender importance, and content urgency.
Always respond with valid JSON matching the required schema.
"""

CATEGORY_SYSTEM_PROMPT = """
Classify emails into categories: Work, Personal, Spam, Newsletter, Support or Other.
Consider the sender, content, and purpose of the email.
Always respond with valid JSON matching the required schema.
"""

INFO_SYSTEM_PROMPT = """
You are an expert at extracting key information from emails.
Identify the sender's intent, whether action is required, urgency indicators and key phrases.
Be precise and extract only relevant information.
Always respond with valid JSON matching the required schema.
"""

def get_priority_prompt(email_content: str) -> str:
    """Generate prompt for priority classification."""
    return f"""
    Analyze the priority of the following email:

    Email Content:
    {email_content}

    Classify the priority as High, Medium, or Low and provide a confidence score.
    """

def get_category_prompt(email_content: str) -> str:
    """Generate prompt for category classification."""
    return f"""
    Categorize the following email:

    Email Content:
    {email_content}

    Classify the email into one of these categories: Work, Personal, Spam, Newsletter, Support, or Other.
    Provide a confidence score.
    """

def get_info_prompt(email_content: str) -> str:
    """Generate prompt for information extraction."""
    return f"""
    Extract key information from the following email:

    Email Content:
    {email_content}

    Identify:
    - The sender's main intent or purpose
    - Whether any action is required from the recipient
    - Any urgency indicators (phrases, words or patterns)
    - Key pharses or important keywords
    """