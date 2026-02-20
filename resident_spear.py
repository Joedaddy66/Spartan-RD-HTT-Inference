import os
import time
import smtplib
import firebase_admin
from firebase_admin import credentials, firestore
from google import genai
from email.mime.text import MIMEText

# --- EMPIRE CONFIGURATION ---
# We force the script to pull the key directly to avoid the 'Missing key' error
# GOOGLE_API_KEY takes precedence in the 2026 SDK
api_key_env = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key_env:
    raise ValueError("❌ EMPIRE ERROR: Terminal keys are set but Python can't see them. Try: export GOOGLE_API_KEY='your_key'")

# 1. INITIALIZE CLIENT (Explicitly passing the key)
ai_client = genai.Client(api_key=api_key_env)

# 2. INITIALIZE MEMORY (Firestore)
PROJECT_ID = "srol-spartan-research"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

if not firebase_admin._apps:
    firebase_admin.initialize_app()
db = firestore.client()

print("🛡️ Nexus Handshake Complete: AI & Memory Online.")

# ... (The rest of your watchdog/pitch code)
