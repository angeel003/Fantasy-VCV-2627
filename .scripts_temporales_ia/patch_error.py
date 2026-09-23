import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'msgBox\.innerText = "Error de conexión\.";', r'msgBox.innerText = "Error: " + err.message;', html)
html = re.sub(r'msgBox\.innerText = "Error de conexi.n\.";', r'msgBox.innerText = "Error: " + err.message;', html)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

