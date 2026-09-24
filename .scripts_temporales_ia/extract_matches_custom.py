import urllib.request
import json

groups = [
    {'id': 87, 'team_name': 'Universidad de Valladolid VCV', 'cat_name': 'SM2'},
    {'id': 100, 'team_name': 'VALCYL VCV', 'cat_name': '1ª Nacional Masc.'},
    {'id': 237, 'team_name': 'Valladolid CV Vacceas', 'cat_name': '1ª Nacional Fem.'}
]

vcv_keywords = ['valladolid', 'vcv', 'valcyl', 'vacceas']

output_lines = []
output_lines.append("ID_Partido\tRonda_Global\tEquipo_Local\tRival\tJornada_Eq\tFecha\tUbicacion\tEstado\tVisibilidad\tCategoria\tPabellon")

for group in groups:
    url = f"https://rfevb.fontventa.com/api/competiciones/getJornadasCalendario?grupoId={group['id']}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    raw = urllib.request.urlopen(req).read()
    data = json.loads(raw.decode('utf-8', errors='replace'))
    
    if 'content' not in data: continue
    
    for jornada in data['content']:
        j_num = jornada['numero']
        for match in jornada.get('partidos', []):
            eq_loc = match['equipo_local'].replace('\ufffd', 'ó')
            eq_vis = match['equipo_visitante'].replace('\ufffd', 'ó')
            
            is_vcv_local = any(kw.lower() in eq_loc.lower() for kw in vcv_keywords)
            is_vcv_vis = any(kw.lower() in eq_vis.lower() for kw in vcv_keywords)
            
            if is_vcv_local or is_vcv_vis:
                id_partido = f"RFEVB_{match['id']}"
                
                if is_vcv_local:
                    equipo_vcv = group['team_name']
                    rival = eq_vis
                    ubicacion = 'LOCAL'
                else:
                    equipo_vcv = group['team_name']
                    rival = eq_loc
                    ubicacion = 'VISITANTE'
                    
                fecha = match.get('fecha_hora', '').replace('\ufffd', 'á') # Sáb.
                pabellon = match.get('pabellon', '') or ''
                pabellon = pabellon.replace('\ufffd', 'Ó')
                
                estado = 'ABIERTO'
                visibilidad = 'MOSTRAR'
                
                pabellon = pabellon.replace('\n', ' ').replace('\r', '').strip()
                rival = rival.replace('\n', ' ').replace('\r', '').strip()
                
                # Manual overrides for specific words if the replace was wrong
                rival = rival.replace('Dumbróa', 'Dumbría').replace('Guóa', 'Guía').replace('Emevó', 'Emevé').replace('ENTREVó?AS', 'ENTREVÍAS').replace('ENTREVóAS', 'ENTREVÍAS')
                
                line = f"{id_partido}\t{j_num}\t{equipo_vcv}\t{rival}\t{j_num}\t{fecha}\t{ubicacion}\t{estado}\t{visibilidad}\t{group['cat_name']}\t{pabellon}"
                output_lines.append(line)

with open('partidos_vcv.txt', 'w', encoding='utf-8-sig') as f:
    f.write('\n'.join(output_lines))

with open('partidos_vcv.csv', 'w', encoding='utf-8-sig') as f:
    f.write('\n'.join([line.replace('\t', ';') for line in output_lines]))

print("Success")

