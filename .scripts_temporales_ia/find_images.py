import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

imgs = re.findall(r'<img[^>]+src="([^">]+)"', text)
print("Images found:")
for img in set(imgs):
    print(img)
