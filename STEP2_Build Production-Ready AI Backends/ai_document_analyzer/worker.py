from curses import meta
import time
from celery import Celery
from pathlib import Path
from config import get_redis_url
from utils import (
    extract_text_from_file,
    analyze_text_with_ai, generate_report,
    save_analysis_result,
    get_file_type
)

REDIS_URL = get_redis_url()

# Setup celery app
celery_app = Celery("document_analyzer",
                    broker=REDIS_URL,
                    backend=REDIS_URL)

# Configure celery
celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(bind=True)
def process_document(self, document_id: str, file_path: str, user_id: str, filename: str):
    """Process a document: extract text, analyze, generate report"""
    try:
        print(f"📄 WORKER: Starting processing for document {document_id}")
        file_path_obj = Path(file_path)
        file_type = get_file_type(filename)

        # Uploading
        self.update_state(state="UPLOADING", meta={"progress": "10%", "message": "File received and validated"})
        time.sleep(0.5) # Simulate work

        # Extracting
        self.update_state(state="EXTRACTING", meta={"progress": "30%", "message": "Extracting text from document"})
        print(f"📄 WORKER: Extracting text from {filename}")

        extracted_text = extract_text_from_file(file_path_obj, file_type)

        if not extracted_text or len(extracted_text.strip() < 10):
            raise ValueError("Could not extract meaningful text from document")

        time.sleep(1) # Simulate work

        # Analyzing
        self.update_state(state="ANALYZING", meta={"progress": "60%", "message": "Analyzing text with AI"})
        print(f"📄 WORKER: Analyzing text (length: {len(extracted_text)} chars)")
        analysis = analyze_text_with_ai(extracted_text)
        time.sleep(1) # SImulate AI processing

        self.update_state(state="GENERATING REPORT", meta={"progress": "90%", "message": "Generating analysis report"})
        print(f"📄 WORKER: Generating report")
        report = generate_report(analysis, document_id)

        # Save result to disk
        save_analysis_result(document_id, report)
        time.sleep(0.5)

        print(f"✅ WORKER: Document {document_id} processing complete!")
        return report
    except Exception as e:
        print(f"❌ WORKER ERROR: {str(e)}")
        # Re-raise to mark task as FAILURE
        raise