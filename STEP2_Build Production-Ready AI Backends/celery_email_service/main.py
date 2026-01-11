from fastapi import FastAPI
from endpoints import email_router
import uvicorn

app = FastAPI(title="Email Service", version="1.0.0")
app.include_router(email_router, prefix="/api/v1/email", tags=["email"])

@app.get("/")
async def health_check():
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
