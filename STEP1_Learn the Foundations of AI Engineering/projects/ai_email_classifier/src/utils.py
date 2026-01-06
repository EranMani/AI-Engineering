from pathlib import Path

def read_email_file(file_path: str) -> str:
    """Read email content from a file"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Email file not found: {file_path}")

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"Email file is empty: {file_path}")

    return content

def validate_email_content(content: str) -> None:
    """Validate email content"""
    if not content or not content.strip():
        raise ValueError("Email content cannot be empty!")

    if len(content) > 100000:
        raise ValueError("Email content is too long!")

    if len(content.strip()) < 10:
        raise ValueError("Email content is too short (minimum 10 characters)!")