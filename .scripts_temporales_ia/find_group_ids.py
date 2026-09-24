import urllib.request
import re
import json

urls = [
    'https://esvoley.es/voleibol/competiciones-masculinas/superliga-masculina-2/grupo-c',
    'https://esvoley.es/voleibol/competiciones-masculinas/primera-division-masculina/grupo-a',
    'https://esvoley.es/voleibol/competiciones-femeninas/primera-division-femenina/grupo-d'
]

# We need the match calendar from API. Let's see what group ID is for each URL
for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    match = re.search(r'constanteValorGrupo\s*=\s*(\d+)', html)
    if not match or match.group(1) == '0':
        # Search for another initialization
        match = re.search(r'init\s*\(\s*(\d+)\s*\)', html)
    
    # Actually, often the ID is in a hidden input or data attribute or initialized in a script
    id_matches = re.findall(r'/api/competiciones/partidos/(\d+)', html)
    print(f"URL: {url}")
    print("API Endpoint IDs found:", id_matches)
    
    # Or let's just find any /partidos/ endpoint call in the script block
    script_match = re.search(r'API_BASE\s*\+\s*\'/jornadas/(\d+)\'', html)
    if script_match:
        print("Jornadas ID:", script_match.group(1))
        
    script_match2 = re.search(r'let valorGrupoId\s*=\s*\'(\d+)\'', html)
    if script_match2:
        print("valorGrupoId:", script_match2.group(1))

    # look at all `var idGrupo = 'XXX'`
    group_id_match = re.search(r'var idGrupo\s*=\s*[\'"]?(\d+)[\'"]?', html)
    if group_id_match:
         print("var idGrupo:", group_id_match.group(1))
    
    # Actually, in fontventa Vue/JS they usually embed the ID in a meta tag or a hidden div
    print("Hidden inputs:", re.findall(r'<input type="hidden"[^>]+value="(\d+)"[^>]*>', html))
    
    # Another way: extract the whole script and look for any hardcoded ID
    # print(re.findall(r'(\d{2,})', html))

