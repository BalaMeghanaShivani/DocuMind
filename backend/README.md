# ⚙️ DocuMind Backend

Powered by **Python FastAPI** for high-performance AI processing.

## Components
- **API**: FastAPI
- **AI Agent**: LangChain / OpenAI
- **Storage**: Sanity CMS integration

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Run: `uvicorn main:app --reload`

## Endpoints
- `POST /upload`: Handle file/voice upload
- `POST /process`: Trigger AI structuring
- `GET /documents`: Retrieve processed docs
