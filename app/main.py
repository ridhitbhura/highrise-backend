from fastapi import FastAPI
from app.routes import router
import uvicorn
import os

# Initialize the app
app = FastAPI(
    title="Highrise FAQ Chatbot API",
    description="Backend for the Highrise FAQ chatbot",
    version="1.0.0"
)

# Include routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Highrise FAQ Chatbot API!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", default=8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
