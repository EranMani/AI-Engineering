from pathlib import Path

def read_text_file(file_path: str) -> str:
    """Read and return contents of a text file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return path.read_text(encoding="utf-8")

def validate_text(text: str, min_length: int = 10) -> bool:
    """Validate text meets minimum requirements."""
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    if len(text.strip()) < min_length:
        raise ValueError(f"Text must be at least {min_length} characters")
    return True