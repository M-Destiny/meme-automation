from PIL import Image, ImageDraw, ImageFont
import os

class Editor:
    def __init__(self, font_path="Impact.ttf"):
        # Note: User might need to provide the font or we can use a system font path
        # Assuming common Linux/Mac/Windows path or just Impact.ttf in project root
        self.font_path = font_path

    def add_text_to_image(self, image_path, top_text, bottom_text, output_path="meme.png"):
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        # Scaling font size based on image width
        font_size = int(w / 12)
        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except OSError:
            print(f"Font not found at {self.font_path}, using default.")
            font = ImageFont.load_default()

        def draw_outline_text(text, position, anchor="mt"):
            # Black outlines
            outline_range = 2
            for x_offset in range(-outline_range, outline_range + 1):
                for y_offset in range(-outline_range, outline_range + 1):
                    draw.text((position[0] + x_offset, position[1] + y_offset), text, font=font, fill="black", anchor=anchor)
            # White main text
            draw.text(position, text, font=font, fill="white", anchor=anchor)

        # Top text
        draw_outline_text(top_text.upper(), (w / 2, 10), anchor="mt")
        # Bottom text
        draw_outline_text(bottom_text.upper(), (w / 2, h - font_size - 10), anchor="ms")
        
        img.save(output_path)
        print(f"Meme saved to {output_path}")
        return output_path

if __name__ == "__main__":
    e = Editor()
    # e.add_text_to_image("generated_image.png", "Top text", "Bottom text")
