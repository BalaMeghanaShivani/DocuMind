
import requests
import json
import time

API_URL = "http://localhost:8000"

def stress_test_complex_prd():
    print("🚀 Starting Complex PRD Stress Test...")
    
    # 1. Complex Input Text (Simulating a chaotic PRD dump)
    raw_text = """
    PRD DRAFT: Project Titan - AI Document Analysis System v2.0
    
    Overview:
    We need to build a system that takes messy documents and turns them into gold. It should handle PDFs, Word docs, and audio files.
    The goal is to reduce manual data entry by 90%.
    
    Problem Statement:
    Current process is manual. Users copy-paste from emails into Excel. Errors are high (15%).
    Competitors are faster. We need to beat DocuSign's new AI features.
    
    Core Features needed for MVP:
    1. Multi-modal ingestion (Text, Audio, PDF).
    2. Intelligent Classification: Must distinguish between Invoices, Contracts, and Meeting Notes.
    3. Structured Output: JSON format is a must for the API.
    4. PDF Generation: Users crave a clean, branded PDF report.
    
    Non-Functional Requirements:
    - Latency < 2s for text under 1000 words.
    - 99.9% uptime.
    - GDPR compliant storage.
    
    User Stories:
    - As a PM, I want to upload a meeting recording and get a summary PDF.
    - As a Dev, I want API access to the structured data.
    - As a Legal Admin, I want to search for "Force Majeure" clauses across all contracts.
    
    Technical Constraints:
    - Backend: Python/FastAPI
    - LLM: GPT-4o
    - Database: Postgres + Vector Store (ChromaDB?)
    
    Open Questions:
    - Do we need real-time streaming? (Maybe later)
    - Budget for LLM tokens? ($500/mo cap)
    """

    print(f"\n📝 Sending {len(raw_text)} chars of text to /process-text...")
    
    payload = {
        "text": raw_text,
        "source_type": "stress_test_script"
    }

    try:
        start_time = time.time()
        response = requests.post(f"{API_URL}/process-text", json=payload)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! (Took {end_time - start_time:.2f}s)")
            print(f"   Doc Type Identified: {data.get('doc_type')}")
            print(f"   Title: {data.get('title')}")
            print(f"   PDF Path: {data.get('pdf_path')}")
            
            # Print structured data snippet
            print("\n🔍 Structured Data Preview:")
            print(json.dumps(data.get('structured_data', {}), indent=2)[:500] + "\n... (truncated)")

            # Check if PDF exists via API
            pdf_filename = data.get('pdf_path').split('/')[-1]
            print(f"\n📥 Attempting to download PDF: {pdf_filename}")
            
            pdf_response = requests.get(f"{API_URL}/download/{pdf_filename}")
            if pdf_response.status_code == 200:
                print(f"✅ PDF Download Successful ({len(pdf_response.content)} bytes)")
                # Optionally save it locally to verify
                with open(f"downloaded_{pdf_filename}", "wb") as f:
                    f.write(pdf_response.content)
                print(f"   Saved to: downloaded_{pdf_filename}")
            else:
                print(f"❌ PDF Download Failed: {pdf_response.status_code}")
                
        else:
            print(f"❌ API Request Failed: {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Is the server running? (uvicorn main:app --reload)")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    stress_test_complex_prd()
