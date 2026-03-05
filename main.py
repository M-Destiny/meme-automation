import os
from dotenv import load_dotenv
from src.brainstormer import Brainstormer
from src.generator import Generator
from src.editor import Editor
from src.publisher import Publisher

load_dotenv()

def run_meme_automation(topic):
    # 1. Brainstorm
    brainstormer = Brainstormer()
    concept = brainstormer.brainstorm(topic)
    if not concept:
        print("Failed to brainstorm meme concept.")
        return

    print(f"Concept: {concept}")

    # 2. Generate
    generator = Generator()
    image_path = generator.generate_image(concept["image_prompt"])
    
    # 3. Edit
    editor = Editor()
    meme_path = editor.add_text_to_image(image_path, concept["top_caption"], concept["bottom_caption"])
    
    # 4. Publish
    # publisher = Publisher()
    # publisher.login()
    # publisher.upload_photo(meme_path, f"Meme about {topic}! #meme #ai")
    
    print(f"Done! Meme created: {meme_path}")

if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "coding bugs"
    run_meme_automation(topic)
