import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add credentials: 'omit' to all fetch options
html = html.replace("method: 'POST', body:", "credentials: 'omit', method: 'POST', body:")

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

