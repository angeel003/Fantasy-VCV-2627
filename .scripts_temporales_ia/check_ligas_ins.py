import re
with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('if (shName === "Ligas" && params.ligas_seleccionadas')
print(text[max(0, idx-200):idx+500])
