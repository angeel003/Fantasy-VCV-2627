import re
with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('tituloPrincipalSeccion')
print(html[max(0, idx-200):idx+500].encode('ascii', 'ignore').decode())

