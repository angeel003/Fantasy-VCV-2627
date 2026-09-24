import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove CSS block
html = re.sub(
    r'\s*/\* ESTILOS DEL JUGADOR DESTACADO \*/.*?\.mvp-quote \{.*?\n    \}',
    '',
    html, flags=re.DOTALL
)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

