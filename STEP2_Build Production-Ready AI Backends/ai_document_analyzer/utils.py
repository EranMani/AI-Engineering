import os
import uuid
import json
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import UploadFile
from config import get_upload_dir, get_results_dir, get_max_file_size
from datetime import datetime

def get_file_type(filename: str) -> str:
    """Detect file type from filename extension"""
    ext = Path(filename).suffix.lower()

    if ext == ".pdf":
        return "pdf"
    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
        return 'image'
    elif ext in ['.txt', '.md', '.doc', '.docx']:
        return 'text'
    else:
        return 'unknown'

def validate_file(file: UploadFile) -> bool:
    """Validate uploaded file"""
    file_type = get_file_type(file.filename)
    if file_type == "unknown":
        return False

    return True

async def save_uploaded_file(file: UploadFile, user_id: str) -> Path:
    """Save uploaded file to disk"""
    upload_dir = get_upload_dir()

    # create user specific directory
    user_dir = upload_dir / user_id
    user_dir.mkdir(parents=True, exist_ok=True)

    file_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix
    file_path = user_dir / f"{file_id}{file_ext}"

    # save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return file_path

def extract_text_from_file(file_path: Path, file_type: str) -> str:
    """Extract text from file based on type"""
    if file_type == 'text':
        # simple text file reading
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    elif file_type == "pdf":
        # pdf text extraction
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            return "[PDF extraction required PYPDF2: pip install PyPDF2]"
    
    elif file_type == "image":
        # OCR for images
        try:
            import pytesseract
            from PIL import Image
            image = Image.open(file_path)
            return pytesseract.image_to_string(image)
        except ImportError:
            return "[OCR required pytessearct and pillow: pip install pytesseract pillow]"
    else:
        return "[Unsupported file type]"

def analyze_text_with_ai(text: str) -> Dict[str, Any]:
    """Analyze text using AI. for now returns a simple analysis"""
    words = text.split()
    sentences = text.split('.')

    summary = text[:200] + "...." if len(text) > 200 else text

    # Extract key points (sentences with more then 10 words)
    key_points = [
        s.strip for s in sentences if len(s.split()) > 10
    ][:5] # limit to 5 key points

    # very simple basic sentiment
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst']

    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    if positive_count > negative_count:
        sentiment = "positive"
    elif negative_count > positive_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "summary": summary,
        "key_points": key_points,
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "sentiment": sentiment,
        "language": "en"
    }

def generate_report(analysis: Dict[str, Any], document_id: str) -> Dict[str, Any]:
    """
    Generate a formatted report from analysis results.
    """
    
    report = {
        "document_id": document_id,
        "summary": analysis["summary"],
        "key_points": analysis["key_points"],
        "word_count": analysis["word_count"],
        "sentence_count": analysis["sentence_count"],
        "sentiment": analysis["sentiment"],
        "language": analysis["language"],
        "metadata": {
            "analyzed_at": datetime.utcnow().isoformat(),
            "analysis_version": "1.0"
        },
        "created_at": datetime.utcnow()
    }
    
    return report

def save_analysis_result(document_id: str, result: Dict[str, Any]) -> Path:
    """Save analysis result to disk"""
    results_dir = get_results_dir()
    result_file = results_dir / f"{document_id}.json"

    with open(result_file, "w") as f:
        json.dump(result, f, indent=2, default=str)

    return result_file

def load_analysis_result(document_id: str) -> Optional[Dict[str, Any]]:
    """Load analysis result from disk"""
    results_dir = get_results_dir()
    result_file = results_dir / f"{document_id}.json"

    if not result_file.exists():
        return None

    with open(result_file, "r") as f:
        return json.load(f)
