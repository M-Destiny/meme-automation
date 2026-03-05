import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

class Generator:
    def __init__(self):
        token = os.getenv("HF_TOKEN")
        self.client = InferenceClient(
            model="stabilityai/stable-diffusion-xl-base-1.0",
            token=token
        )

    def generate_image(self, prompt, output_path="generated_image.png"):
        print(f"Generating image for prompt: {prompt}")
        image_bytes = self.client.text_to_image(prompt)
        # image_bytes is a PIL image object directly
        image_bytes.save(output_path)
        print(f"Image saved to {output_path}")
        return output_path

if __name__ == "__main__":
    g = Generator()
    g.generate_image("A futuristic cat coding on a laptop")
