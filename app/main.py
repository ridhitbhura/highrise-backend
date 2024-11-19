from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
import os

# Environment configuration
PORT = int(os.getenv("PORT", 10000))

app = FastAPI(
    title="Highrise FAQ Chatbot API",
    description="Backend for the Highrise FAQ chatbot",
    version="1.0.0"
)

# CORS middleware setup for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.get("/")
def read_root():
    """
    Root endpoint providing basic API information.
    
    Returns:
        dict: Basic API information and configuration
    """
    return {
        "message": "Welcome to the Highrise FAQ Chatbot API!",
        "port": PORT,
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Health status and port information
    """
    return {"status": "healthy", "port": PORT}
