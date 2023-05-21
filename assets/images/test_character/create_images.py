from PIL import Image

# Create a list of colors ranging from red to blue
colors = [(255, 0, 0), (235, 64, 52), (214, 128, 102), (193, 191, 153), (128, 191, 204),
          (77, 166, 255), (64, 128, 255), (51, 64, 235), (38, 0, 215), (25, 0, 192)]

folders = ['blunderbuss_lose', 'blunderbuss_win', 'idle', 'lose', 'win']

for folder in folders:
    # Create images with the colors and save them in a folder
    for i, color in enumerate(colors):
        img = Image.new('RGB', (500, 500), color=color)
        img.save(f'{folder}/{i}.png')
