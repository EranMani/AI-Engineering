from fastapi import FastAPI
from router import api_router

# init the application
app = FastAPI(title="My AI Backend test")

# connect the master router
app.include_router(api_router)

# root check to see if the server is alive
@app.get("/")
def health_check():
    return {"status": "running", "message": "AI Backend is online"}