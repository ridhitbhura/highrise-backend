from fastapi import FastAPI
from app.routes import router

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
