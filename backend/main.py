"""
🚀 DocuMind API — FastAPI Application
AI-powered document automation: ingest text/voice → structure → PDF.
"""

import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

from models import (
    TextProcessRequest,
    DocumentResponse,
    TranscribeResponse,
    HealthResponse,
    ErrorResponse,
    IntegrationStatusResponse,
)
from core.pipeline import process_document_pipeline
from services.deepgram import deepgram_client
from services.sanity import sanity_client
from core.config import OPENAI_API_KEY, DEEPGRAM_API_KEY, FOXIT_CLIENT_ID, SANITY_TOKEN


# ==========================================
# 🏗 App Setup
# ==========================================

app = FastAPI(
    title="DocuMind API",
    description=(
        "AI-powered document automation. "
        "Ingest raw text or voice recordings, classify and structure them "
        "with an AI agent, and generate professional PDFs."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow all origins for hackathon flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# ⚠️ Global Exception Handler
# ==========================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all handler that returns a consistent ErrorResponse."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="internal_server_error",
            detail=str(exc),
        ).model_dump(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler for FastAPI HTTPExceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=f"http_{exc.status_code}",
            detail=exc.detail,
        ).model_dump(),
    )


# ==========================================
# 📡 Endpoints
# ==========================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health check",
)
async def health_check():
    """Returns service health status."""
    return HealthResponse()


@app.post(
    "/process-text",
    response_model=DocumentResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Processing failure"},
    },
    tags=["Documents"],
    summary="Process raw text into a structured document",
)
async def process_text(request: TextProcessRequest):
    """
    Accepts raw text (meeting notes, PRD, code docs, etc.)
    and returns AI-structured content with a generated PDF path.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text input cannot be empty.")

    try:
        result = process_document_pipeline(request.text, request.source_type)
        return DocumentResponse(
            doc_type=result["doc_type"],
            title=result["title"],
            structured_data=result["structured_data"],
            pdf_path=result["pdf_path"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline processing failed: {str(e)}",
        )


@app.post(
    "/transcribe-audio",
    response_model=TranscribeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file"},
        500: {"model": ErrorResponse, "description": "Transcription failure"},
    },
    tags=["Audio"],
    summary="Transcribe an audio file to text",
)
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    """
    Accepts an audio file upload (.mp3, .wav, etc.),
    transcribes it via Deepgram, and returns the transcript.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    
    # Validate file type
    allowed_types = {
        "audio/mpeg", "audio/wav", "audio/mp3",
        "audio/x-wav", "audio/ogg", "audio/webm",
        "application/octet-stream",  # fallback for unknown types
    }
    if file.content_type and file.content_type not in allowed_types:
         print(f"⚠️ Warning: potentially unsupported file type {file.content_type}")

    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # Real Deepgram Call
        result = deepgram_client.transcribe_bytes(content, file.filename)
        
        transcript_text = result.get("formatted_transcript", "") or result.get("transcript", "")
        
        if not transcript_text:
             raise HTTPException(status_code=500, detail="Transcription failed to return text.")

        return TranscribeResponse(
            transcript=transcript_text,
            structured_data=result 
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Transcription endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# 🏃‍♂️ Entry Point
# ==========================================

@app.get("/documents")
async def get_documents(doc_type: str = None):
    """Fetches list of generated documents from Sanity."""
    return sanity_client.get_documents(doc_type)

@app.get("/documents/tasks")
async def get_open_tasks():
    """Fetches all open action items from Sanity documents."""
    return sanity_client.get_open_tasks()

@app.get(
    "/integrations/status",
    response_model=IntegrationStatusResponse,
    tags=["System"],
    summary="Check integration connection status",
)
async def get_integration_status():
    """Checks if API keys are configured for external services."""
    return IntegrationStatusResponse(
        openai="connected" if OPENAI_API_KEY else "missing",
        deepgram="connected" if DEEPGRAM_API_KEY else "missing",
        foxit="connected" if FOXIT_CLIENT_ID else "missing",
        sanity="connected" if SANITY_TOKEN else "missing",
    )


@app.get("/", tags=["System"])
async def root():
    """Root endpoint to verify the server is running."""
    return {
        "message": "DocuMind API is running!",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Serves generated PDF files."""
    file_path = os.path.join("output", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, media_type='application/pdf', filename=filename)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
