import re
with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('"ligas":')
if idx == -1: idx = text.find('ligas:')
if idx == -1: idx = text.find('Ligas')
print(text[max(0, idx-500):idx+1500].encode('ascii', 'ignore').decode())

