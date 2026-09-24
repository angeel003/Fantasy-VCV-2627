import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="displayJugador"')
idx_end = text.find('<form id="prediccionForm">')
print(text[max(0, idx-200):idx_end].encode('utf-8').decode('utf-8', 'ignore'))

