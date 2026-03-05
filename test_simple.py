import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

try:
    response = client.models.generate_content(
        model="gemma-3-1b-it", contents="Hello"
    )
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
