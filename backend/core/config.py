import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 🔑 API Keys & Configuration
# Centralized place to manage all environment variables.

# OpenAI (AI Agent)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Deepgram (Voice to Text)
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Foxit PDF Services (Document Generation & Enhancement)
# Get credentials from: https://developers.foxit.com/
FOXIT_CLIENT_ID = os.getenv("FOXIT_CLIENT_ID")
FOXIT_CLIENT_SECRET = os.getenv("FOXIT_CLIENT_SECRET")

# Sanity CMS (Storage)
SANITY_PROJECT_ID = os.getenv("SANITY_PROJECT_ID")
SANITY_DATASET = os.getenv("SANITY_DATASET", "production")
SANITY_TOKEN = os.getenv("SANITY_TOKEN")

# App Settings
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
