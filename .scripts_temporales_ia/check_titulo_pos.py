import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="tituloPrincipalSeccion"')
print(text[max(0, idx-100):idx+300])

