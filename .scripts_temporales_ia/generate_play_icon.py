import os
from PIL import Image, ImageDraw

def create_play_icon():
    # 64x64 transparent image
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a purple triangle (VCV purple is #783b7a -> 120, 59, 122)
    # Points for a right-pointing triangle
    points = [(16, 12), (16, 52), (52, 32)]
    draw.polygon(points, fill=(120, 59, 122, 255))
    
    os.makedirs('files/images', exist_ok=True)
    img.save('files/images/play_icon.png')

create_play_icon()

