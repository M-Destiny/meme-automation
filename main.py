import os
from dotenv import load_dotenv
from src.brainstormer import Brainstormer
from src.generator import Generator
from src.editor import Editor
from src.publisher import InstaPublisher, MetaPublisher

load_dotenv()

def run_meme_automation(topic, use_meta_api=False):
    # 1. Brainstorm
    brainstormer = Brainstormer()
    concept = brainstormer.brainstorm(topic)
    if not concept:
        print("Failed to brainstorm meme concept.")
        return

    print(f"Concept: {concept}")

    # 2. Generate
    import time
    timestamp = int(time.time())
    os.makedirs("assets/temp", exist_ok=True)
    raw_path = f"assets/temp/raw_{timestamp}.png"
    generator = Generator()
    image_path = generator.generate_image(concept["image_prompt"], output_path=raw_path)
    
    # 3. Edit
    os.makedirs("assets/generated", exist_ok=True)
    meme_path = f"assets/generated/comicon_meme_{timestamp}.png"
    editor = Editor()
    meme_path = editor.add_text_to_image(image_path, concept["top_caption"], concept["bottom_caption"], output_path=meme_path)
    
    # 4. Commit and Push
    print(f"Committing and pushing meme to GitHub...")
    os.system(f"git add {meme_path} && git commit -m 'Add generated meme {timestamp}' && git push origin main")

    # 5. Publish
    if use_meta_api:
        publisher = MetaPublisher()
        # Meta API needs a public URL, this might fail with local paths
        # publisher.upload_photo("http://your-server.com/" + meme_path, f"Meme about {topic}! #meme #ai #punecomicon")
        print("MetaPublisher selected. Note: Official API requires a public image URL.")
    else:
        publisher = InstaPublisher()
        if publisher.login():
            publisher.upload_photo(meme_path, f"Meme about {topic}! #meme #ai #punecomicon")
    
    print(f"Done! Meme created: {meme_path}")

if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "coding bugs"
    # Set this to True to use Meta Graph API
    use_meta = os.getenv("USE_META_API", "false").lower() == "true"
    run_meme_automation(topic, use_meta_api=use_meta)
