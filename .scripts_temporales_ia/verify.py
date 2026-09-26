import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
print(re.search(r'<section id="enlacesRfevbSection"[^>]*>', text).group(0))
print(re.search(r'<span>Mis predicciones</span>', text).group(0))
