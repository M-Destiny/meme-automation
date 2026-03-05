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
        Generate a highly detailed Poster/Meme concept for 'Pune Comicon'.
        
        Theme: Focus heavily on {topic} (Anime, Gaming, Harry Potter, etc.) mashed up with Pune culture.
        Specific Context: Pune Comicon vibe, cosplay, local landmarks (Shaniwar Wada), 
        local food (Misal Pav, Puran Poli), Pune traffic, and the fan convention experience.
        
        Requirements:
        1. image_prompt: A high-quality, vibrant poster-style prompt for Stable Diffusion XL. 
           Mention 'highly detailed', 'cinematic lighting', and 'comic book style'.
        2. top_caption: A catchy, SHORT title or hook.
        3. bottom_caption: A funny or epic sub-caption that fits the Pune context.
        4. description: A fun Instagram caption.
        5. tags: A string of hashtags.

        CRITICAL: Keep captions concise so they don't overflow the image.

        Respond ONLY with valid JSON.
        """
        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )
        try:
            content = response.text.strip().replace("```json", "").replace("```", "")
            return json.loads(content)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            print(f"Raw response: {response.text}")
            return None


if __name__ == "__main__":
    b = Brainstormer()
    print(json.dumps(b.brainstorm("coding bugs"), indent=2))
