"""
📦 DocuMind API Models
Pydantic schemas for request validation and response serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from datetime import datetime


# ==========================================
# 📥 Request Models
# ==========================================

class TextProcessRequest(BaseModel):
    """Request body for POST /process-text"""
    text: str = Field(
        ...,
        min_length=1,
        description="Raw text to process (meeting notes, PRD, code docs, etc.)"
    )
    source_type: str = Field(
        default="text",
        description="Source type: 'text' or 'voice'"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Team Meeting - Oct 27\nAgenda:\n1. Review Q3 metrics\nAction Items:\n- Sarah to email stakeholders",
                    "source_type": "text"
                }
            ]
        }
    }


# ==========================================
# 📤 Response Models
# ==========================================

class DocumentResponse(BaseModel):
    """Response for successfully processed documents."""
    success: bool = True
    doc_type: str = Field(..., description="Detected document type")
    title: str = Field(..., description="Inferred document title")
    structured_data: Dict[str, Any] = Field(
        ..., description="AI-structured content as JSON"
    )
    pdf_path: Optional[str] = Field(
        None, description="Path to generated PDF (if available)"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Processing timestamp"
    )


class TranscribeResponse(BaseModel):
    """Response for audio transcription."""
    success: bool = True
    transcript: str = Field(..., description="Transcribed text from audio")
    structured_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Structured content (if auto-processing was applied)"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Processing timestamp"
    )

class IntegrationStatusResponse(BaseModel):
    """Response for GET /integrations/status."""
    openai: str = Field(..., description="Status of OpenAI integration")
    deepgram: str = Field(..., description="Status of Deepgram integration")
    foxit: str = Field(..., description="Status of Foxit integration")
    sanity: str = Field(..., description="Status of Sanity integration")


class HealthResponse(BaseModel):
    """Response for GET /health."""
    status: str = "healthy"
    service: str = "DocuMind API"
    version: str = "1.0.0"
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class ErrorResponse(BaseModel):
    """Standard error response envelope."""
    success: bool = False
    error: str = Field(..., description="Error type or code")
    detail: str = Field(..., description="Human-readable error message")
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )
