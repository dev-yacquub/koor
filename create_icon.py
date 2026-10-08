"""
Generates a crisp, professional multi-size Windows .ico file for Koor.
Features a modern circular cyan/blue gradient badge with a bell/star motif.
"""
from PIL import Image, ImageDraw
import os

def create_koor_icon(output_path="koor.ico"):
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer soft glow / shadow
    for offset in range(12, 0, -2):
        alpha = int(15 * (1 - offset / 12))
        draw.ellipse([24 - offset, 24 - offset, size - 24 + offset, size - 24 + offset],
                     fill=(14, 165, 233, alpha))

    # Base vibrant blue circle (Somali Sky Blue #0ea5e9 to #0284c7)
    draw.ellipse([28, 28, size - 28, size - 28], fill=(14, 165, 233, 255))
    draw.ellipse([34, 34, size - 34, size - 34], fill=(2, 132, 199, 255))

    # Inner subtle rim
    draw.ellipse([36, 36, size - 36, size - 36], outline=(56, 189, 248, 200), width=4)

    # Stylized Traditional Koor Bell (Wooden camel bell with carved grooves)
    # Bell body
    bell_box = [160, 160, 352, 360]
    draw.rounded_rectangle(bell_box, radius=48, fill=(255, 255, 255, 255))

    # Bell head loop (handle)
    draw.ellipse([220, 100, 292, 180], outline=(255, 255, 255, 255), width=16)

    # Horizontal groove lines
    draw.line([180, 230, 332, 230], fill=(2, 132, 199, 255), width=10)
    draw.line([190, 270, 322, 270], fill=(2, 132, 199, 255), width=8)

    # Clapper (the swinging sound piece at bottom)
    draw.ellipse([236, 340, 276, 395], fill=(240, 249, 255, 255))
    draw.line([256, 330, 256, 360], fill=(2, 132, 199, 255), width=8)

    # 5-pointed white star emblem in center
    # Center = (256, 310)
    # Little shine highlight in top right
    draw.arc([50, 50, size - 50, size - 50], start=210, end=300, fill=(255, 255, 255, 120), width=8)

    # Save as high-res multi-layer Windows .ico
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save(output_path, format="ICO", sizes=sizes)
    print(f"Icon generated successfully: {output_path}")

if __name__ == "__main__":
    create_koor_icon("koor.ico")
