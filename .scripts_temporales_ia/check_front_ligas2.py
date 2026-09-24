import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('ligas_seleccionadas')
print(text[max(0, idx-200):idx+500].encode('ascii', 'ignore').decode())

