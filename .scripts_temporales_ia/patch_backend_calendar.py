import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    code = f.read()

# Find the block where `cartelera` is defined and returned in `login` (or `get_data`)
# and add `todosPartidos`.

inject_code = """
        var cartelera = [];
        var todosPartidos = [];
        for(var i=0; i<partidos.length; i++) { 
            if(partidos[i].permitido) {
                todosPartidos.push(partidos[i]);
                if(partidos[i].visibilidad === "MOSTRAR") {
                    cartelera.push(partidos[i]);
                }
            } 
        }

        // ASOCIAR STREAMING A CADA PARTIDO
        for (var c = 0; c < cartelera.length; c++) {
            var cp = cartelera[c];
            var oRes = resultadosMap[cp.id_partido];
            cp.streaming = (oRes && oRes.streaming) ? oRes.streaming : "";
        }
        for (var c = 0; c < todosPartidos.length; c++) {
            var tp = todosPartidos[c];
            var oRes = resultadosMap[tp.id_partido];
            tp.streaming = (oRes && oRes.streaming) ? oRes.streaming : "";
        }
"""

old_code = """        var cartelera = [];
        for(var i=0; i<partidos.length; i++) { if(partidos[i].visibilidad === "MOSTRAR" && partidos[i].permitido) { cartelera.push(partidos[i]); } }

        // ASOCIAR STREAMING A CADA PARTIDO
        for (var c = 0; c < cartelera.length; c++) {
            var cp = cartelera[c];
            var oRes = resultadosMap[cp.id_partido];
            cp.streaming = (oRes && oRes.streaming) ? oRes.streaming : "";
        }"""

code = code.replace(old_code, inject_code)

# Add it to the JSON response
old_json = '"equipos": cartelera,'
new_json = '"equipos": cartelera, "todos_partidos": todosPartidos,'
code = code.replace(old_json, new_json)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(code)
print("Patched script-dev")

