import os
import json

from google import genai
from dotenv import load_dotenv

load_dotenv()


class Brainstormer:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemma-3-1b-it"

    def brainstorm(self, topic: str) -> dict | None:
        prompt = f"""
        Generate a JSON object for a 'Pune Comicon 2026' poster/meme.
        Theme: {topic} (Gaming, Anime, Harry Potter, etc.)
        Culture: Pune (landmarks, food, traffic).
        
        Respond ONLY with a JSON object in this format:
        {{
          "image_prompt": "cinematic highly detailed 8k prompt about characters from {topic} in Pune",
          "top_caption": "SHORT Title",
          "bottom_caption": "Funny Pune sub-caption",
          "description": "Fun IG caption",
          "tags": "#tags #hashtags"
        }}
        """
        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )
        try:
            text = response.text.strip()
            # Find the first { and last } to extract JSON
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                content = text[start:end+1]
                return json.loads(content)
            return None
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            print(f"Raw response: {response.text}")
            return None


if __name__ == "__main__":
    b = Brainstormer()
    print(json.dumps(b.brainstorm("coding bugs"), indent=2))
