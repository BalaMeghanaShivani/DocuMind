import json
from enum import Enum
from typing import Dict, Any

from services.llm import llm_service
from services.foxit import foxit_client
from services.sanity import sanity_client

# ==========================================
# 🧠 DocuMind Core Pipeline
# ==========================================

class DocumentType(Enum):
    MEETING_NOTES = "meeting_notes"
    PRD = "product_requirements"
    CODE_DOCS = "code_documentation"
    UNKNOWN = "general"

def process_document_pipeline(raw_input: str, source_type: str = "text") -> Dict[str, Any]:
    """
    Core pipeline to transform raw input into structured data + PDF.
    """
    
    print(f"🚀 Starting pipeline for source: {source_type}")

    # 1. Ingest & Preprocess
    clean_text = raw_input.strip()
    
    # 2. Detect Document Type
    print("🔍 Classifying document...")
    doc_type_str = llm_service.classify_text(clean_text)
    try:
        doc_type = DocumentType(doc_type_str)
    except ValueError:
        doc_type = DocumentType.UNKNOWN
    
    print(f"📋 Detected Document Type: {doc_type.value}")

    # 3. Structure Content
    print("🧠 Structuring content with AI...")
    structured_data = llm_service.structure_text(clean_text, doc_type.value)
    
    # 4. Generate PDF
    print(f"📄 Generating PDF via Foxit API...")
    raw_pdf_path = foxit_client.generate_pdf_from_html(structured_data, doc_type.value)
    
    # 5. Enhance PDF (Foxit Integration)
    try:
        final_pdf_path = foxit_client.enhance_pdf(raw_pdf_path)
    except Exception:
        final_pdf_path = raw_pdf_path
    
    print(f"✅ Document ready at: {final_pdf_path}")
    
    # 6. Save to Sanity CMS
    try:
        print(f"💾 Saving to Sanity CMS...")
        sanity_client.create_document(
            doc_type=doc_type.value,
            title=structured_data.get("title", "Untitled Document"),
            structured_data=structured_data,
            pdf_path=final_pdf_path
        )
    except Exception as e:
        print(f"⚠️ Sanity Save Failed (Non-blocking): {e}")

    return {
        "doc_type": doc_type.value,
        "title": structured_data.get("title", "Untitled Document"),
        "structured_data": structured_data,
        "pdf_path": final_pdf_path,
    }

