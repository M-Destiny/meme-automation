"""Quick flow test: Brainstorm -> Generate -> Edit. No Instagram posting."""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from src.brainstormer import Brainstormer
from src.generator import Generator
from src.editor import Editor

def test_flow(topic: str = "Pune Comicon cosplay"):
    print("=" * 50)
    print(f"🧠 Step 1: Brainstorming meme about '{topic}'...")
    print("=" * 50)
    b = Brainstormer()
    concept = b.brainstorm(topic)
    if not concept:
        print("❌ Brainstorming failed!")
        return
    print(f"✅ Concept: {json.dumps(concept, indent=2)}")

    print("\n" + "=" * 50)
    print("🎨 Step 2: Generating image...")
    print("=" * 50)
    g = Generator()
    img_path = g.generate_image(concept["image_prompt"], output_path="assets/temp/test_generated.png")
    print(f"✅ Image saved: {img_path}")

    print("\n" + "=" * 50)
    print("✍️  Step 3: Adding meme text...")
    print("=" * 50)
    e = Editor()
    meme_path = e.add_text_to_image(
        img_path,
        concept["top_caption"],
        concept["bottom_caption"],
        output_path="assets/temp/test_meme.png",
    )
    print(f"✅ Meme saved: {meme_path}")
    print("\n🎉 Flow test complete!")

if __name__ == "__main__":
    os.makedirs("assets/temp", exist_ok=True)
    topic = sys.argv[1] if len(sys.argv) > 1 else "Pune Comicon cosplay"
    test_flow(topic)
