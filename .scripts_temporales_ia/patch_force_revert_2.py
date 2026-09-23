import re
with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Completely remove the script tag containing LÓGICA DE CACHÉ
html = re.sub(r'<script>\s*// LÓGICA DE CACHÉ V2[\s\S]*?</script>', '', html)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

