import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

class Brainstormer:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def brainstorm(self, topic):
        prompt = f"""
        Generate a funny meme concept based on the topic: '{topic}'.
        Provide the response in JSON format with the following keys:
        - image_prompt: A descriptive prompt for an image generator (like Stable Diffusion).
        - top_caption: Funny text for the top of the meme.
        - bottom_caption: Funny text for the bottom of the meme.
        """
        response = self.model.generate_content(prompt)
        # Basic JSON parsing from the response text
        try:
            # Cleaning potential markdown formatting
            content = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(content)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return None

if __name__ == "__main__":
    b = Brainstormer()
    print(b.brainstorm("coding bugs"))
