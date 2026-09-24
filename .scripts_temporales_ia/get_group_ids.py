import urllib.request
import re

urls = [
    'https://esvoley.es/voleibol/competiciones-masculinas/superliga-masculina-2/grupo-c',
    'https://esvoley.es/voleibol/competiciones-masculinas/primera-division-masculina/grupo-a',
    'https://esvoley.es/voleibol/competiciones-femeninas/primera-division-femenina/grupo-d'
]

ids = []
for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'id="HiddenGrupoId" type="hidden" value="(\d+)"', html)
    if match:
        ids.append(match.group(1))
    else:
        ids.append(None)
print("Grupo IDs:", ids)

