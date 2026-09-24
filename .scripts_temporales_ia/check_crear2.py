import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('crearUsuarioAdmin')
print(text[max(0, idx-50):idx+500].encode('ascii', 'ignore').decode())
