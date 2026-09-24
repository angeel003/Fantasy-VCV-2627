import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Revert cache: 'no-store' but KEEP the ?t= timestamp cache buster
html = html.replace("{ cache: 'no-store', ", "{ ")

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

