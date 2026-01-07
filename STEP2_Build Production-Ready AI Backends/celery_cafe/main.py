from fastapi import FastAPI
from router import api_router

app = FastAPI(
    title="Celery Cafe Production",
    description="A high-throughput cafe simulation using FastAPI and Celery",
    version="1.0.0"
)

# Connect the master router to the app
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "Cafe is OPEN"}