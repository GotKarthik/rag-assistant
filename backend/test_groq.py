import sys
from app.config import settings
from groq import Groq

api_key = settings.groq_api_key
print(f"API Key configured: {'Yes' if api_key else 'No'}")
if not api_key or api_key == "your_groq_api_key_here":
    print("Error: API Key is missing or default.")
    sys.exit(1)

print("Testing API Key...")
try:
    client = Groq(api_key=api_key)
    models = client.models.list()
    print("API Key is VALID! Successfully fetched models.")
except Exception as e:
    print(f"API Key is INVALID or failed to connect: {e}")
