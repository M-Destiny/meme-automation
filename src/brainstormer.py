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
        Act as a creative director for 'Pune Comicon 2026' (March 21-22, 2026).
        Create a visually engaging poster or meme concept.
        
        Theme: {topic} (Choose one: Gaming, Anime, or Harry Potter if not specific).
        
        Requirements for the Image Prompt:
        - Gaming: popular icons/characters/controllers with Pune landmarks backdrop.
        - Anime: well-known characters/elements, vibrant colors, integrated Pune landmarks.
        - Harry Potter: magical visuals (wands, Hogwarts, spells) with subtle references to Pune’s skyline/landmarks.
        
        Respond ONLY with a JSON object in this format:
        {{
          "theme_type": "gaming or anime or magic",
          "image_prompt": "cinematic highly detailed 8k prompt following the requirements above",
          "description": "Playful and dynamic Instagram caption for the Comicon audience",
          "tags": "#PuneComicon2026 #Pune #Comicon #Anime #Gaming #HarryPotter"
        }}
        """
        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )
        try:
            text = response.text.strip()
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                content = text[start:end+1]
                data = json.loads(content)
                # Construct the fixed captions based on the user's specific requirement
                data["top_caption"] = "Pune Comicon 2026"
                theme = data.get("theme_type", "magic").lower()
                data["bottom_caption"] = f"Experience the magic of {theme} at Pune Comicon! March 21-22, Pune!"
                return data
            return None
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return None


if __name__ == "__main__":
    b = Brainstormer()
    print(json.dumps(b.brainstorm("coding bugs"), indent=2))
