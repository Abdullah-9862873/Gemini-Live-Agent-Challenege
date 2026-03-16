# AI Multimodal Tutor - How to Run

## Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- API keys (see below)

## Setup API Keys

Edit `.env` file in the root directory:

```env
# Required
PINECONE_API_KEY=your_pinecone_api_key
GEMINI_API_KEY=your_gemini_api_key
GITHUB_REPO=owner/repository-name

# Optional (for deployment)
GOOGLE_CLOUD_PROJECT=your_project_id
```

Get keys from:
- Pinecone: https://app.pinecone.io/
- Gemini: https://aistudio.google.com/app/apikey

---

## Running the Backend

### Option 1: Direct Python (Recommended for development)

```bash
# Navigate to backend folder
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install gTTS for voice output
pip install gtts

# Run the server
uvicorn main:app --reload
```

The API will be running at: http://localhost:8000

### Option 2: Docker

```bash
# Build the Docker image
docker build -t ai-tutor-backend ./backend

# Run the container
docker run -p 8000:8000 --env-file .env ai-tutor-backend
```

---

## Running the Frontend

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be running at: http://localhost:3000

---

## Testing the API

### 1. Check Health
```bash
curl http://localhost:8000/health
```

### 2. Ingest Course Content
```bash
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{"repo": "microsoft/vscode", "extensions": [".md", ".py"]}'
```

### 3. Ask a Question
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is merge sort?", "top_k": 5}'
```

### 4. API Documentation
Visit http://localhost:8000/docs for interactive API docs

---

## Quick Start Commands Summary

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install gtts
uvicorn main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

Then open http://localhost:3000 in your browser.
