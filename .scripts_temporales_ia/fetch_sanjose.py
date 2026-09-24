import urllib.request
import json
import traceback

url = 'https://www.rfevb.com/RFEVB/FrontVenta.aspx/GetPartidos'
data = json.dumps({"id_grupo": 237}).encode('utf-8')
headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, data=data, headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        partidos = res.get('d', [])
        print(f"Loaded {len(partidos)} matches")
        
        matches_found = []
        for p in partidos:
            eq_loc = p.get('Eq_loc', '')
            eq_vis = p.get('Eq_vis', '')
            
            # Look for San Jose matches
            if 'san jos' in eq_loc.lower() or 'san jos' in eq_vis.lower():
                # Format to txt format
                # ID_Partido	Ronda_Global	Equipo_Local	Rival	Jornada_Eq	Fecha	Ubicacion	Estado	Visibilidad	Categoria	Pabellon
                id_partido = f"RFEVB_{p.get('id_partido')}"
                ronda_global = p.get('Jornada')
                jornada_eq = p.get('Jornada')
                
                fecha = p.get('Fecha', '')
                hora = p.get('Hora', '')
                fecha_str = f"{fecha} {hora}" if fecha else ""
                
                is_sj_local = 'san jos' in eq_loc.lower()
                equipo_local = eq_loc if is_sj_local else eq_vis
                rival = eq_vis if is_sj_local else eq_loc
                ubicacion = 'LOCAL' if is_sj_local else 'VISITANTE'
                
                # IMPORTANT: Replace encoding issues
                equipo_local = equipo_local.replace('\ufffd', 'ó').replace('\xd3', 'Ó').replace('\xed', 'í')
                rival = rival.replace('\ufffd', 'ó').replace('\xd3', 'Ó').replace('\xed', 'í')
                pabellon = p.get('Pabellon', '').replace('\ufffd', 'ó').replace('\xd3', 'Ó')
                
                matches_found.append(f"{id_partido}\t{ronda_global}\tCD San José\t{rival}\t{jornada_eq}\t{fecha_str}\t{ubicacion}\tABIERTO\tMOSTRAR\t1ª Nacional Fem.\t{pabellon}")
        
        print(f"Found {len(matches_found)} San Jose matches")
        with open('partidos_sj.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(matches_found) + "\n")
            
except Exception as e:
    print('Error:', traceback.format_exc())

