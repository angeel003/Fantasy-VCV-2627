import urllib.request
import json
import traceback

group_id = 237

url = f"https://rfevb.fontventa.com/api/competiciones/getJornadasCalendario?grupoId={group_id}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

matches_found = []

try:
    with urllib.request.urlopen(req) as response:
        res = response.read().decode('utf-8')
        data = json.loads(res)
        
        if 'content' in data:
            for jornada in data['content']:
                j_num = jornada['numero']
                for match in jornada.get('partidos', []):
                    eq_loc = match['equipo_local']
                    eq_vis = match['equipo_visitante']
                    
                    is_sj_local = 'san jos' in eq_loc.lower() or 's. jos' in eq_loc.lower()
                    is_sj_vis = 'san jos' in eq_vis.lower() or 's. jos' in eq_vis.lower()
                    
                    if is_sj_local or is_sj_vis:
                        id_partido = f"RFEVB_{match['id']}"
                        
                        # ID_Partido	Ronda_Global	Equipo_Local	Rival	Jornada_Eq	Fecha	Ubicacion	Estado	Visibilidad	Categoria	Pabellon
                        # From previous custom script, user wanted exactly: CD San José
                        equipo_local = "CD San José"
                        
                        if is_sj_local:
                            rival = eq_vis
                            ubicacion = "LOCAL"
                        else:
                            rival = eq_loc
                            ubicacion = "VISITANTE"
                            
                        # Fix encoding issues for rival
                        rival = rival.replace('\ufffd', 'ó').replace('\xd3', 'Ó').replace('\xed', 'í')
                        
                        # Sometimes CD San Jose plays Valladolid CV Vacceas
                        # If rival is Valladolid CV Vacceas, we still extract it for San Jose if the user wants it!
                        # Wait, the RFEVB extraction might have already added it for VCV?
                        # The user said: "añadeselos al final del otro txt"
                        if 'vacce' in rival.lower() or 'vcv' in rival.lower() or 'valladolid' in rival.lower():
                            rival = "Valladolid CV Vacceas" # Match exactly the team name from before
                            
                        fecha = match.get('fecha_hora', '')
                        pabellon = match.get('pabellon', '').replace('\ufffd', 'ó').replace('\xd3', 'Ó')
                        
                        matches_found.append(f"{id_partido}\t{j_num}\t{equipo_local}\t{rival}\t{j_num}\t{fecha}\t{ubicacion}\tABIERTO\tMOSTRAR\t1ª Nacional Fem.\t{pabellon}")
                        
        with open('partidos_sj.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(matches_found) + "\n")
            
        print(f"Found {len(matches_found)} CD San José matches and saved to partidos_sj.txt")
except Exception as e:
    print('Error:', traceback.format_exc())

