import urllib.request
import json

groups = [
    {'id': 87, 'name': 'Superliga 2 Masculina'},
    {'id': 100, 'name': 'Primera Masculina'},
    {'id': 237, 'name': 'Primera Femenina'}
]

vcv_keywords = ['valladolid', 'vcv']

output_lines = []

for group in groups:
    url = f"https://rfevb.fontventa.com/api/competiciones/getJornadasCalendario?grupoId={group['id']}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    
    if 'content' not in data: continue
    
    for jornada in data['content']:
        j_num = jornada['numero']
        for match in jornada.get('partidos', []):
            eq_loc = match['equipo_local']
            eq_vis = match['equipo_visitante']
            
            is_vcv_local = any(kw.lower() in eq_loc.lower() for kw in vcv_keywords)
            is_vcv_vis = any(kw.lower() in eq_vis.lower() for kw in vcv_keywords)
            
            if is_vcv_local or is_vcv_vis:
                id_partido = f"RFEVB_{match['id']}"
                
                if is_vcv_local:
                    equipo_vcv = group['name']
                    rival = eq_vis
                    ubicacion = 'LOCAL'
                else:
                    equipo_vcv = group['name']
                    rival = eq_loc
                    ubicacion = 'VISITANTE'
                    
                fecha = match.get('fecha_hora', '')
                pabellon = match.get('pabellon', '') or ''
                estado = 'ABIERTO'
                visibilidad = 'MOSTRAR'
                
                # Strip weird characters or normalize
                pabellon = pabellon.replace('\n', ' ').replace('\r', '').strip()
                rival = rival.replace('\n', ' ').replace('\r', '').strip()
                
                line = f"{id_partido}\t{j_num}\t{equipo_vcv}\t{rival}\t{j_num}\t{fecha}\t{ubicacion}\t{estado}\t{visibilidad}\t{group['name']}\t{pabellon}"
                output_lines.append(line)

with open('partidos_vcv_utf8bom.txt', 'w', encoding='utf-8-sig') as f:
    f.write('\n'.join(output_lines))

