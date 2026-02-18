import os
import json
from openai import OpenAI
from core.config import OPENAI_API_KEY

class LLMService:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        if not self.api_key:
            print("⚠️ OpenAI API Key missing. LLM features will fail.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

    def classify_text(self, text: str) -> str:
        """
        Classifies input text into one of: 'meeting_notes', 'prd', 'code_docs'.
        """
        if not self.client:
            return "general"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a classifier. Output ONLY one of these strings: 'meeting_notes', 'prd', 'code_docs'. If unsure, 'general'."},
                    {"role": "user", "content": f"Classify this text:\n\n{text[:1000]}"}
                ],
                temperature=0.0
            )
            return response.choices[0].message.content.strip().lower()
        except Exception as e:
            print(f"❌ LLM Classification Failed: {e}")
            return "general"

    def structure_text(self, text: str, doc_type: str) -> dict:
        """
        Extracts structured data from text based on doc_type.
        """
        if not self.client:
            return {"title": "Untitled", "summary": text[:200]}

        from backend.core.prompts import SYSTEM_PROMPT
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"DOCUMENT TYPE: {doc_type}\n\nINPUT TEXT:\n{text}"}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"❌ LLM Structuring Failed: {e}")
            return {"title": "Error Parsing", "error": str(e)}

# Singleton
llm_service = LLMService()
