from PIL import Image, ImageDraw, ImageFont
import os
import requests


FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf"
FONT_FILE = os.path.join(FONT_DIR, "BebasNeue-Regular.ttf")


def ensure_font():
    """Download Bebas Neue (Google Font) if not already present."""
    if os.path.exists(FONT_FILE):
        return FONT_FILE
    os.makedirs(FONT_DIR, exist_ok=True)
    print(f"Downloading Bebas Neue font from Google Fonts...")
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

        # Scaling font size - smaller to avoid overflow
        font_size = int(w / 16)
        # Branding font even smaller to be safe
        try:
            font = ImageFont.truetype(self.font_path, font_size)
            branding_font = ImageFont.truetype(self.font_path, int(font_size * 0.5))
        except OSError:
            print(f"Font not found at {self.font_path}, using default.")
            font = ImageFont.load_default()
            branding_font = ImageFont.load_default()

        def draw_outline_text(text: str, position: tuple, anchor: str = "mt", custom_font=None):
            f = custom_font or font
            # Wrap text to fit width (safer char width)
            avg_char_width = (f.getlength("W") if hasattr(f, "getlength") else font_size) * 0.6
            max_chars = max(1, int((w * 0.90) / avg_char_width))
            import textwrap
            wrapped_text = "\n".join(textwrap.wrap(text, width=max_chars))
            
            # Calculate total text height
            bbox = draw.multiline_textbbox(position, wrapped_text, font=f, align="center")
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            
            # Adjust position
            adj_x = position[0] - text_w / 2
            if anchor == "mt":
                adj_y = position[1]
            elif anchor == "mb":
                adj_y = position[1] - text_h
            else:
                adj_y = position[1]

            outline = max(2, font_size // 30)
            for xo in range(-outline, outline + 1):
                for yo in range(-outline, outline + 1):
                    draw.multiline_text(
                        (adj_x + xo, adj_y + yo),
                        wrapped_text,
                        font=f,
                        fill="black",
                        align="center"
                    )
            draw.multiline_text((adj_x, adj_y), wrapped_text, font=f, fill="white", align="center")

        # Top text
        draw_outline_text(top_text.upper(), (w / 2, 40), anchor="mt")
        
        # Bottom text (pushed up to clear branding)
        draw_outline_text(bottom_text.upper(), (w / 2, h - 120), anchor="mb")
        
        # Mandatory PUNE COMICON branding (MB anchor to grow UPWARD from margin)
        draw_outline_text("PUNE COMICON 2026", (w / 2, h - 30), anchor="mb", custom_font=branding_font)

        final = img.convert("RGB")
        final.save(output_path)
        print(f"Meme saved to {output_path}")
        return output_path


if __name__ == "__main__":
    e = Editor()
    # e.add_text_to_image("generated_image.png", "Top text", "Bottom text")
