import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd()))
from core.pipeline import process_document_pipeline

if __name__ == "__main__":
    print("🧪 Testing Foxit Integration in Pipeline...")
    
    sample_text = """
    Team Meeting - Oct 27
    Agenda: 
    1. Review Q3 metrics
    2. Plan Q4 Roadmap
    Action Items:
    - Sarah to email stakeholders
    """
    
    try:
        result = process_document_pipeline(sample_text)
        print("\n✅ Pipeline Result:")
        print(f"Doc Type: {result['doc_type']}")
        print(f"PDF Path: {result['pdf_path']}")
        
        # Verify file exists
        if os.path.exists(result['pdf_path']):
             print(f"✅ File exists at {result['pdf_path']}")
             print(f"   Size: {os.path.getsize(result['pdf_path'])} bytes")
        else:
             print(f"❌ File missing at {result['pdf_path']}")

    except Exception as e:
        print(f"\n❌ Pipeline Failed: {e}")
        import traceback
        traceback.print_exc()
