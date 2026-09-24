import re

files = ['script-dev/Código.js', 'script-prod/Código.js']

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        js = f.read()
    
    # 1. First, we need to extract the keys from misPermisos that are true.
    # Where is misPermisos created?
    # It's at the beginning of the `login` block.
    # var misPermisos = {}; 
    
    # Let's just find the JSON return and inject mis_equipos_siguiendo
    old_json = '"equipos_totales": misEquiposTotales,'
    
    # We can create `misEquiposSiguiendo` array right before the return statement.
    old_return = 'var rondaAbierta = sheetAjustes.getRange("B2").getValue() || "1";'
    new_return = '''var rondaAbierta = sheetAjustes.getRange("B2").getValue() || "1";
        
        var misEquiposSiguiendo = [];
        for(var eqq in misPermisos) {
            if(misPermisos[eqq] === true) misEquiposSiguiendo.push(eqq);
        }
'''
    
    new_json = '"mis_equipos_siguiendo": misEquiposSiguiendo,\n            "equipos_totales": misEquiposTotales,'
    
    if old_return in js and old_json in js:
        js = js.replace(old_return, new_return)
        js = js.replace(old_json, new_json)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(js)
        print(f"Patched backend {filename}")
    else:
        print(f"Tokens not found in {filename}!")

