import os
from PIL import Image, ImageDraw

def add_corners(im, rad, is_circle=False):
    # Ensure image is RGBA
    im = im.convert("RGBA")
    
    # Create white background
    white_bg = Image.new("RGBA", im.size, "WHITE")
    # Paste transparent image onto white background
    white_bg.paste(im, (0, 0), im)
    im = white_bg
    
    # Create mask
    mask = Image.new('L', im.size, 0)
    draw = ImageDraw.Draw(mask)
    if is_circle:
        draw.ellipse((0, 0, im.size[0], im.size[1]), fill=255)
    else:
        draw.rounded_rectangle((0, 0, im.size[0], im.size[1]), radius=rad, fill=255)
    
    result = Image.new('RGBA', im.size, (0,0,0,0))
    result.paste(im, (0, 0), mask=mask)
    return result

input_path = "files/images/logo_vcv_tiny.png"
if os.path.exists(input_path):
    im = Image.open(input_path)
    # 20% rounding for rounded corners
    radius = int(min(im.size) * 0.2)
    
    img_rounded = add_corners(im, radius, is_circle=False)
    img_rounded.save("files/images/logo_vcv_rounded.png")
    
    img_circle = add_corners(im, radius, is_circle=True)
    img_circle.save("files/images/logo_vcv_circle.png")
    
    print("Icons generated successfully!")
else:
    print("Input file not found.")

