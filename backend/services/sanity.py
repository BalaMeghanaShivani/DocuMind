import requests
import json
import uuid
from datetime import datetime
from core.config import SANITY_PROJECT_ID, SANITY_DATASET, SANITY_TOKEN

class SanityClient:
    def __init__(self):
        self.project_id = SANITY_PROJECT_ID
        self.dataset = SANITY_DATASET
        self.token = SANITY_TOKEN
        self.base_url = f"https://{self.project_id}.api.sanity.io/v2021-06-07/data"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def create_document(self, doc_type: str, title: str, structured_data: dict, pdf_path: str):
        """
        Creates a new 'generatedDocument' in Sanity.
        """
        if not self.token:
            print("⚠️ Sanity token missing. Skipping storage.")
            return None

        doc_id = str(uuid.uuid4())
        
        # Prepare mutations
        mutations = [
            {
                "create": {
                    "_id": doc_id,
                    "_type": "generatedDocument",
                    "title": title,
                    "docType": doc_type,
                    "createdAt": datetime.now().isoformat(),
                    "summary": structured_data.get("summary", ""),
                    "actionItems": structured_data.get("action_items", []),
                    # Store structured data as a JSON string or map fields if schema allows
                    # For this hackathon, we assume schema has specific fields. 
                    # If schema is flexible, we might store raw JSON.
                    "structuredContent": json.dumps(structured_data), 
                    "pdfUrl": pdf_path # In a real app, upload file -> get asset URL
                }
            }
        ]

        url = f"{self.base_url}/mutate/{self.dataset}"
        
        try:
            response = requests.post(url, headers=self._headers(), json={"mutations": mutations})
            response.raise_for_status()
            print(f"✅ Saved to Sanity: {doc_id}")
            return response.json()
        except Exception as e:
            print(f"❌ Sanity Save Failed: {e}")
            return None

    def get_documents(self, doc_type: str = None):
        """
        Fetches documents using GROQ.
        """
        if not self.token:
            return []

        query = '*[_type == "generatedDocument"] | order(createdAt desc)'
        if doc_type:
            query = f'*[_type == "generatedDocument" && docType == "{doc_type}"] | order(createdAt desc)'
        
        return self._run_query(query)

    def get_open_tasks(self):
        """
        Fetches all unresolved action items.
        Assumes actionItems is an array of objects with a 'status' field.
        """
        if not self.token:
            return []

        # This GROQ query assumes actionItems are objects inside the document
        query = """
        *[_type == "generatedDocument" && count(actionItems) > 0] {
            _id,
            title,
            "tasks": actionItems
        }
        """
        return self._run_query(query)

    def _run_query(self, query: str):
        url = f"{self.base_url}/query/{self.dataset}"
        try:
            response = requests.get(url, headers=self._headers(), params={"query": query})
            response.raise_for_status()
            return response.json().get("result", [])
        except Exception as e:
             print(f"❌ Sanity Query Failed: {e}")
             return []

# Singleton
sanity_client = SanityClient()
