# Highrise FAQ Chatbot Backend

## Description

This is the backend API for the Highrise FAQ chatbot, built using FastAPI.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/chatbot-backend.git
cd chatbot-backend
```

2. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Add OpenAI API key to .env file:

```bash
OPENAI_API_KEY=<your-openai-api-key>
```

4. Run the application:

```bash
uvicorn app.main:app --reload
```

5. Access the API at http://127.0.0.1:8000.
