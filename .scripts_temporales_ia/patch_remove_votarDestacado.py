import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove window.votarDestacado completely
html = re.sub(
    r'window\.votarDestacado = function\(e, idPart\) \{.*?\};\n',
    '',
    html, flags=re.DOTALL
)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

