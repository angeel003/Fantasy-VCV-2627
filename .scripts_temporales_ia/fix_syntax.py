import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('// Observe DOM changes in contenedorPartidos\n    };', '')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Syntax error fixed")
