import re
with open('prototipo_stitch.html', 'r', encoding='utf-8') as f:
    text = f.read()
views = re.findall(r'<section class="view-section[^>]*id="([^"]+)">', text)
print('Vistas encontradas:', views)
