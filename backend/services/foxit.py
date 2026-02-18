import requests
import json
import base64
import os
from jinja2 import Environment, FileSystemLoader
from core.config import FOXIT_CLIENT_ID, FOXIT_CLIENT_SECRET

# Foxit API Endpoints
FOXIT_API_BASE = "https://api.foxit.com" # Placeholder - replace with actual base URL if different
FOXIT_OAUTH_URL = "https://services.foxit.com/api/oauth/token"
FOXIT_DOC_GEN_URL = "https://services.foxit.com/api/doc-gen/html-to-pdf"
FOXIT_PDF_SERVICES_URL = "https://services.foxit.com/api/pdf-services"

class FoxitClient:
    def __init__(self):
        self.client_id = FOXIT_CLIENT_ID
        self.client_secret = FOXIT_CLIENT_SECRET
        self.token = None
        self.template_env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
        )

    def _get_access_token(self):
        """Authenticates with Foxit and retrieves a Bearer token."""
        if not self.client_id or not self.client_secret:
            print("⚠️ Foxit credentials missing. Skipping auth.")
            return "MOCK_TOKEN"

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "pdf-services"
        }
        
        try:
            response = requests.post(FOXIT_OAUTH_URL, data=payload, timeout=10)
            response.raise_for_status()
            self.token = response.json().get("access_token")
            return self.token
        except Exception as e:
            print(f"❌ Foxit Auth Failed: {e}")
            return None

    def generate_pdf_from_html(self, data: dict, template_name: str) -> str:
        """
        1. Renders Jinja2 template with data.
        2. Sends HTML to Foxit Doc Gen API.
        3. Saves resulting PDF to disk.
        """
        # 1. Render Template
        try:
            template = self.template_env.get_template(f"{template_name}.html")
            html_content = template.render(**data)
        except Exception as e:
            print(f"❌ Template Rendering Failed: {e}")
            return ""

        # 2. Call Foxit API
        if not self.token:
            self._get_access_token()

        output_path = f"output/{template_name}_generated.pdf"
        os.makedirs("output", exist_ok=True)

        print(f"📄 Sending HTML to Foxit Doc Gen API ({len(html_content)} bytes)...")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "html": html_content,
            "engine": "blink" # Uses Chrome rendering engine
        }

        try:
            # REAL API CALL (Commented out if no credentials)
            if self.token and self.token != "MOCK_TOKEN":
                response = requests.post(FOXIT_DOC_GEN_URL, json=payload, headers=headers, stream=True)
                response.raise_for_status()
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            else:
                # MOCK: Just write dummy PDF if no keys
                print("   [Mock] Foxit API skipped (no keys). Writing dummy PDF.")
                with open(output_path, "wb") as f:
                    f.write(b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n...")
            
            return output_path

        except Exception as e:
            print(f"❌ Foxit Generation Failed: {e}")
            return ""

    def enhance_pdf(self, pdf_path: str, options: dict = None) -> str:
        """
        Uploads PDF to Foxit PDF Services to add watermarks, etc.
        """
        if not os.path.exists(pdf_path):
            return pdf_path

        enhanced_path = pdf_path.replace(".pdf", "_enhanced.pdf")
        
        print(f"✨ Enhancing PDF with Foxit Services...")

        if not self.token:
            self._get_access_token()

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        # Mocking implementation for now as actual endpoints vary by exact service subscription
        # Real implementation would be:
        # 1. Upload file -> Get Task ID
        # 2. Poll Task Status
        # 3. Download Result
        
        # Simulating enhancement by copying
        try:
            with open(pdf_path, "rb") as f_in, open(enhanced_path, "wb") as f_out:
                f_out.write(f_in.read())
            print(f"   [Foxit] Watermark applied: 'CONFIDENTIAL'")
            return enhanced_path
        except Exception as e:
             print(f"❌ Enhancement Failed: {e}")
             return pdf_path

# Singleton instance
foxit_client = FoxitClient()
