import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the Pre-fetching block
html = re.sub(
    r'\s*// --- PRE-CALENTAMIENTO.*?\}\), 500\);',
    '',
    html, flags=re.DOTALL
)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

