import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('tituloPrincipalSeccion')
while idx != -1:
    print(f"Match at {idx}:")
    print(text[max(0, idx-50):idx+100].encode('ascii', 'ignore').decode())
    idx = text.find('tituloPrincipalSeccion', idx + 1)

