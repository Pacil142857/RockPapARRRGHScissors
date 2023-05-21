from io import BytesIO
import os
from PIL import Image, ImageDraw, ImageFont

# Create a list of colors ranging from red to blue
colors = [(255, 0, 0), (235, 64, 52), (214, 128, 102), (193, 191, 153), (128, 191, 204),
          (77, 166, 255), (64, 128, 255), (51, 64, 235), (38, 0, 215), (25, 0, 192)]

folders = ['blunderbuss_lose', 'blunderbuss_win', 'idle', 'lose', 'win', 'tie']

for folder in folders:
    # Create images with the colors and save them in a folder
    for i, color in enumerate(colors):
        img = Image.new('RGB', (100, 100), color=color)

        center_x = int(img.size[0] / 2) 
        center_y = int(img.size[1] / 2)

        # Add the folder name to the center of the image
        # Add the folder name to the center of the image with smaller font text
        folder_text = os.path.basename(folder)
        draw = ImageDraw.Draw(img)
        font_size = 10

        file = open("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", "rb")
        bytes_font = BytesIO(file.read())
        font = ImageFont.truetype(bytes_font, font_size)

        text_width, text_height = draw.textsize(folder_text, font=font)
        text_x = center_x - int(text_width / 2)
        text_y = center_y - int(text_height / 2)
        draw.text((text_x, text_y), folder_text, fill="black", font=font)

        img.save(f'{folder}/{i}.png')

