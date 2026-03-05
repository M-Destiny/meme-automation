from PIL import Image, ImageDraw, ImageFont
import os
import requests


FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf"
FONT_FILE = os.path.join(FONT_DIR, "Anton-Regular.ttf")


def ensure_font():
    """Download Anton (Google Font) if not already present."""
    if os.path.exists(FONT_FILE):
        return FONT_FILE
    os.makedirs(FONT_DIR, exist_ok=True)
    print(f"Downloading Anton font from Google Fonts...")
    resp = requests.get(FONT_URL, timeout=30)
    resp.raise_for_status()
    with open(FONT_FILE, "wb") as f:
        f.write(resp.content)
    print(f"Font saved to {FONT_FILE}")
    return FONT_FILE


class Editor:
    def __init__(self, font_path: str | None = None):
        self.font_path = font_path or ensure_font()

    def add_text_to_image(
        self,
        image_path: str,
        top_text: str,
        bottom_text: str,
        output_path: str = "meme.png",
    ) -> str:
        img = Image.open(image_path).convert("RGBA")
        draw = ImageDraw.Draw(img)
        w, h = img.size

        # Scaling font size based on image width - making it smaller to avoid overflow
        font_size = int(w / 18)  # Changed from w / 12 to w / 18
        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except OSError:
            print(f"Font not found at {self.font_path}, using default.")
            font = ImageFont.load_default()

        def draw_outline_text(text: str, position: tuple, anchor: str = "mt"):
            # Wrap text to fit width
            avg_char_width = font_size * 0.5
            max_chars = int((w * 0.9) / avg_char_width)
            import textwrap
            wrapped_text = "\n".join(textwrap.wrap(text, width=max_chars))
            
            outline = max(2, font_size // 25)
            for xo in range(-outline, outline + 1):
                for yo in range(-outline, outline + 1):
                    draw.text(
                        (position[0] + xo, position[1] + yo),
                        wrapped_text,
                        font=font,
                        fill="black",
                        anchor=anchor,
                        align="center"
                    )
            draw.text(position, wrapped_text, font=font, fill="white", anchor=anchor, align="center")

        draw_outline_text(top_text.upper(), (w / 2, 10), anchor="mt")
        draw_outline_text(bottom_text.upper(), (w / 2, h - 10), anchor="mb")

        final = img.convert("RGB")
        final.save(output_path)
        print(f"Meme saved to {output_path}")
        return output_path


if __name__ == "__main__":
    e = Editor()
    # e.add_text_to_image("generated_image.png", "Top text", "Bottom text")
