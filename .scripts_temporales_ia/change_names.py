import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Pronóstico de Sets', 'Pronóstico de sets')
text = text.replace('Diferencia de Puntos', 'Diferencia de puntos')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Changed names.")
