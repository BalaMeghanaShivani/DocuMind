
import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.pipeline import process_document_pipeline

def test_pipeline_pdf_generation():
    print("🚀 Testing Full Pipeline PDF Generation...")
    
    # Input text that should trigger 'meeting_notes' classification
    test_text = """
    Meeting: Weekly Sync
    Date: Oct 27, 2026
    Attendees: Alice, Bob
    
    Discussion:
    - Reviewed the new design.
    - Agreed to deploy on Friday.
    
    Action Items:
    - Alice to fix the bug.
    """
    
    try:
        # Run the pipeline
        result = process_document_pipeline(test_text, source_type="test_script")
        
        print("\n✅ Pipeline Finished!")
        print(f"Doc Type: {result['doc_type']}")
        print(f"PDF Path: {result['pdf_path']}")
        
        if result['pdf_path'] and os.path.exists(result['pdf_path']):
            print(f"✅ VERIFIED: PDF file exists at {result['pdf_path']}")
            # Optional: check file size
            size = os.path.getsize(result['pdf_path'])
            print(f"   File size: {size} bytes")
        else:
            print("❌ FAILED: PDF path returned but file missing.")
            
    except Exception as e:
        print(f"❌ Exception during pipeline execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pipeline_pdf_generation()
