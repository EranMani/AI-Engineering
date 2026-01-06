import uuid
import time
import logging
from fastapi import FastAPI, Request, HTTPException
from schemas import UserRequest, SentimentResult
from service import analyze_text

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AIService")

app = FastAPI()

# --- MIDDLEWARE (The Watchdog) ---
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    logger.info(f"[{request_id}] START: {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"[{request_id}] DONE in {process_time:.4f}s")
    
    response.headers["X-Request-ID"] = request_id
    return response

# --- ENDPOINT ---
@app.post("/analyze", response_model=SentimentResult)
def analyze_endpoint(request: UserRequest):
    try:
        # Call the Logic Layer
        result = analyze_text(request.message)
        return result
    except Exception as e:
        logger.error(f"Service Error: {str(e)}")
        raise HTTPException(status_code=500, detail="AI processing failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)