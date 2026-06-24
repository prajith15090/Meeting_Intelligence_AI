import os
from dotenv import load_dotenv

load_dotenv()

NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SENDGRID_API_KEY = os.getenv("SEND_GRID_EMAIL") # Provided as SEND_GRID_EMAIL but is an API Key
SENDGRID_SENDER_EMAIL = os.getenv("SENDGRID_SENDER_EMAIL", "your_email@example.com")
USER_NAME = os.getenv("USER_NAME", "Your Name")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Your Company")
