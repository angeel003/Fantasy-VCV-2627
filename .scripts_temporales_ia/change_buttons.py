import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Entrar al Fantasy', 'Entrar')
text = text.replace('Entrar como Invitado (Solo Lectura)', 'Entrar como invitado')
# Just in case:
text = text.replace('Entrar como Invitado', 'Entrar como invitado')
text = text.replace('Entrar como invitado (Solo Lectura)', 'Entrar como invitado')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Texts replaced.")
