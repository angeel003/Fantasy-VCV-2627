import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

old_visibility_logic = """        if(rTimestamp && nowMs >= (rTimestamp - 15 * 60 * 1000)) { nuevoEstado = "CERRADO"; }
        if((rTimestamp && nowMs >= (rTimestamp + 24 * 60 * 60 * 1000)) || (resultadosMap[idPart] && resultadosMap[idPart].sets)) {
            nuevoEstado = "CERRADO"; nuevaVisibilidad = "OCULTAR";
        }"""

new_visibility_logic = """        if(rTimestamp && nowMs >= (rTimestamp - 15 * 60 * 1000)) { nuevoEstado = "CERRADO"; }
        if(rTimestamp && nowMs >= (rTimestamp + 48 * 60 * 60 * 1000)) {
            nuevoEstado = "CERRADO"; nuevaVisibilidad = "OCULTAR";
        }"""

js_content = js_content.replace(old_visibility_logic, new_visibility_logic)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

