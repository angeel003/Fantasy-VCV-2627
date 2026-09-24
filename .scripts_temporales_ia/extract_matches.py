import urllib.request
import json
import re
from datetime import datetime

groups = [
    {'id': 87, 'name': 'Superliga 2 Masculina'},
    {'id': 100, 'name': 'Primera Masculina'},
    {'id': 237, 'name': 'Primera Femenina'}
]

vcv_keywords = ['valladolid', 'vcv']

output_lines = []
output_lines.append("ID_Partido\tRonda_Global\tEquipo_VCV\tRival\tJornada_Eq\tFecha\tUbicacion\tEstado\tVisibilidad\tCategoria\tPabellon")

# Track global rounds by weekend? Or just use Jornada number?
# The user can adjust Ronda Global in Excel, so we can just use Jornada number as Ronda Global.

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
                
                # Determine VCV team and Rival
                if is_vcv_local:
                    equipo_vcv = group['name'] # or use eq_loc directly? Let's use group name for clarity or eq_loc
                    rival = eq_vis
                    ubicacion = 'LOCAL'
                else:
                    equipo_vcv = group['name']
                    rival = eq_loc
                    ubicacion = 'VISITANTE'
                    
                fecha = match['fecha_hora'] # usually 'DD/MM/YYYY HH:MM'
                
                # Format to match Excel precisely
                pabellon = match.get('pabellon', '')
                estado = 'ABIERTO'
                visibilidad = 'MOSTRAR'
                
                line = f"{id_partido}\t{j_num}\t{equipo_vcv}\t{rival}\t{j_num}\t{fecha}\t{ubicacion}\t{estado}\t{visibilidad}\t{group['name']}\t{pabellon}"
                output_lines.append(line)

with open('partidos_vcv.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"Generated {len(output_lines)-1} matches.")

