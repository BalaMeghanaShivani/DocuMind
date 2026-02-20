
import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.pipeline import process_document_pipeline

def inspect_generated_pdf():
    print("🚀 Running Pipeline to Generate and Inspect PDF...")
    
    test_text = "Test PDF Content"
    
    try:
        # Run pipeline
        result = process_document_pipeline(test_text, source_type="debug_script")
        pdf_path = result['pdf_path']
        
        print(f"\n📄 Generated PDF Path: {pdf_path}")
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"📦 File Size: {file_size} bytes")
            
            with open(pdf_path, "rb") as f:
                header = f.read(20)
                print(f"🔍 File Header (first 20 bytes): {header}")
                
                f.seek(0)
                content = f.read()
                print(f"🔍 Full Content Preview:\n{content[:200]}")
                
            if file_size < 100:
                 print("\n⚠️ WARNING: File size is suspiciously small.")
        else:
            print("❌ PDF file was not created.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inspect_generated_pdf()
