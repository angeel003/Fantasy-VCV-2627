with open('prototipo_stitch.html', 'r', encoding='utf-8') as f:
    text = f.read()
import re
print("Containers:")
matches = re.finditer(r'id="(.*?-container)"', text)
for m in matches:
    print(m.group(1))
print("Other IDs:")
matches = re.finditer(r'id="([^"]+)"', text)
ids = [m.group(1) for m in matches]
print(sorted(list(set(ids))))
