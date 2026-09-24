import os
from PIL import Image

input_path = "files/images/logo_vcv_tiny.png"
im = Image.open(input_path).convert("RGBA")
white_bg = Image.new("RGBA", im.size, "WHITE")
white_bg.paste(im, (0, 0), im)
white_bg.save("files/images/logo_vcv_square_white.png")

