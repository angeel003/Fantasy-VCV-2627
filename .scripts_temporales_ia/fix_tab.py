with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('id="enlacesRfevbSection" style="display:none;', 'id="enlacesRfevbSection" style="')
text = text.replace('>Mis Pronos<', '>Mis predicciones<')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed inline display:none and renamed tab.')
