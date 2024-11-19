from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
import uvicorn
import os

# Initialize the app
app = FastAPI(
    title="Highrise FAQ Chatbot API",
    description="Backend for the Highrise FAQ chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Highrise FAQ Chatbot API!"}
