# Highrise FAQ Chatbot

## Deliverables

### 1. Code and Documentation
- **Main Code**: Located in `app/chatbot.py`
- **Supporting Files**:
  - `app/main.py`: FastAPI backend setup
  - `frontend.py`: NiceGUI frontend implementation
  - `app/faq_scraper.py`: Data collection script
- **Documentation**: Comprehensive inline comments and docstrings in all files

### 2. Sample Interaction Logs
- **Location**: `logs/chat_feedback.log`
- **Format**: JSON entries with timestamps
- **Contents**: Mix of:
  - Supported questions with helpful responses
  - Edge cases and unsupported questions
  - Clarification requests
  - User feedback (helpful/not helpful)

### 3. Deployment History
- **Initial Attempt**: Vercel/Next.js
  - Implemented client-side rendering
  - Faced API credit limitations
  - Performance issues with API integration

- **Secondary Attempt**: Render
  - Deployed backend and frontend separately
  - Attempted optimization with pickle files
  - Limited by request load handling
  - Cost-effective but performance constrained

### 4. Documentation
- Comprehensive README (this file)
- Setup instructions below
- Architecture explanation
- Implementation details
- Future improvements outlined

## Features

- Interactive chat interface
- Real-time responses
- Feedback system
- Link support
- Auto-scrolling
- Environment-based configuration

## Prerequisites

- Python 3.9+
- OpenAI API key

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/highrise-backend.git
cd highrise-backend
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` file in project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
ENVIRONMENT=development
```

Note: PostgreSQL configuration has been replaced with local logging.

## Logging System

The application uses a local logging system to track chat interactions and feedback:

- Location: `logs/chat_feedback.log`
- Format: JSON entries with timestamps
- Tracked attributes:
  - Timestamp
  - Message content
  - Feedback type (helpful/not helpful)
- Automatic log rotation and management

## Running Locally

### Option 1: Using the Script (Recommended)

1. Make the script executable:

```bash
chmod +x run_local.sh
```

2. Run the development servers:

```bash
./run_local.sh
```

### Option 2: Manual Start

1. Start the backend server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

2. In a new terminal, start the frontend:

```bash
python frontend.py
```

## Accessing the Application

- Frontend Chatbot: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

### Backend Development

The backend uses FastAPI and includes:

- REST API endpoints
- Database integration
- OpenAI integration
- Error handling
- Logging

### Frontend Development

The frontend uses NiceGUI and includes:

- Real-time chat interface
- Feedback system
- Link support
- Auto-scrolling
- Environment-based configuration

## Environment Variables

### Required Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `ENVIRONMENT`: 'development' or 'production'

### Optional Variables

- `PORT`: Server port (default: 8000 for backend, 3000 for frontend)
- `BACKEND_URL`: URL of backend service (default: http://localhost:8000)

## Common Issues

### Port Already in Use

```bash
# Kill process on port 8000
sudo lsof -t -i:8000 | xargs kill -9

# Kill process on port 3000
sudo lsof -t -i:3000 | xargs kill -9
```

### Database Connection Issues

1. Verify PostgreSQL is running
2. Check DATABASE_URL format
3. Ensure database exists
4. Verify user permissions

### OpenAI API Issues

1. Verify API key is valid
2. Check API key has sufficient credits
3. Ensure proper environment variable setup

## Implementation History

### FAQ Data Collection

- Implemented custom FAQ scraper:
  - Python-based web scraper using BeautifulSoup4
  - Targeted Highrise knowledge base articles
  - Structured data extraction:
    - Questions
    - Answers
    - Article URLs
    - Categories
  - Data cleaning and formatting
  - Export to JSON format (`highrise_faq.json`)

### Database Evolution

- Initially implemented PostgreSQL for feedback storage
- Transitioned to local logging system for simplicity:
  - JSON-formatted log files
  - Timestamp-based entries
  - Feedback tracking
  - Message attribute storage

### RAG Implementation

- Implemented Retrieval-Augmented Generation (RAG) for more accurate responses
- Faced challenges with:
  - OpenAI API credit limitations
  - Query response times
  - Embedding storage and retrieval

### Hosting Attempts

- Vercel/Next.js

  - Implemented client-side rendering
  - Faced performance issues with API integration
  - Credit limitations affected sustainability

- Render (Backend & Frontend)
  - Successfully deployed both services
  - Attempted pickle file optimization for data loading
  - Encountered scalability issues with request load
  - Cost-effective but performance limited

## Future Improvements

### Hosting & Infrastructure

- Evaluate enterprise-grade hosting solutions:
  - Heroku
  - AWS
  - Render with upgraded resources

### Frontend Architecture

- Rebuild as client-side rendered application
  - Next.js for improved performance
  - Better state management
  - Optimized API calls

### Enhanced RAG Implementation

- Vector database integration with Pinecone
  - Improved embedding storage
  - Faster query responses
  - Cost-effective scaling
- Optimize embedding loaders
- Implement caching strategies
- Consider alternative vector DBs

## Additional Requirements

For FAQ scraping:

```bash
pip install beautifulsoup4
pip install requests
pip install html5lib
```

## Data Collection

### FAQ Scraping Process

1. Run the FAQ scraper:

```bash
python app/faq_scraper.py
```

2. The scraper will:

   - Fetch articles from Highrise knowledge base
   - Parse HTML content
   - Extract relevant information
   - Clean and structure the data
   - Save to `data/highrise_faq.json`

3. Scraping configuration:
   - Rate limiting to respect server limits
   - Error handling for failed requests
   - Data validation
   - Duplicate detection
   - Category-based organization
