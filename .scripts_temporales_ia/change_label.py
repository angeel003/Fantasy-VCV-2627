import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('PUNTOS DIFERENCIAL', 'DIFERENCIA DE PUNTOS')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Changed label.")
