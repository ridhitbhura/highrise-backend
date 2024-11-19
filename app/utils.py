import logging
import pickle
from app.models import Base, engine

def setup_logging():
    """Configure logging settings."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("chatbot.log"),
            logging.StreamHandler()
        ]
    )

def save_embeddings(embeddings, file_path):
    """Save embeddings to a file."""
    with open(file_path, "wb") as f:
        pickle.dump(embeddings, f)

def load_embeddings(file_path):
    """Load embeddings from a file."""
    with open(file_path, "rb") as f:
        return pickle.load(f)

def init_db():
    """Initialize the database by creating tables."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
