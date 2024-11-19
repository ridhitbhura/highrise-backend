from fastapi import APIRouter, HTTPException
from app.models import SessionLocal, Log
from app.chatbot import SimpleFAQChatbot
from app.models import Query, Feedback

# Initialize router and chatbot
router = APIRouter()
chatbot = SimpleFAQChatbot("data/highrise_faq.json")

def log_to_database(question: str, answer: str, feedback: str = None):
    """Log interactions to the database."""
    db = SessionLocal()
    try:
        log = Log(question=question, answer=answer, feedback=feedback)
        db.add(log)
        db.commit()
    except Exception as e:
        print(f"Error logging to database: {e}")
    finally:
        db.close()

@router.post("/ask")
async def ask_question(query: Query):
    """Handle user questions."""
    try:
        response = chatbot.ask(query.question)
        log_to_database(question=query.question, answer=response)
        return {"question": query.question, "answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
async def log_feedback(feedback: Feedback):
    """Log user feedback."""
    try:
        log_to_database(
            question=feedback.question,
            answer="",
            feedback=feedback.feedback
        )
        return {"message": "Feedback logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
