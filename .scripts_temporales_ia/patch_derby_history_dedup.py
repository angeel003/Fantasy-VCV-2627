import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    js = f.read()

old_permitido = 'partidos[p].permitido = (misPermisos[eqLoc] === true);'
new_permitido = 'partidos[p].permitido = (misPermisos[partidos[p].equipo_local] === true || misPermisos[partidos[p].rival] === true);'

js = js.replace(old_permitido, new_permitido)

# Also fix get_history deduplication!
# get_history iterates over partidos! It will output TWO history cards if Excel has two rows!
old_hist_loop = """    if (action === "get_history") {
        var miHistorial = [];
        var matchdaysMap = {};
        for(var i=0; i<partidos.length; i++) {"""

new_hist_loop = """    if (action === "get_history") {
        var miHistorial = [];
        var matchdaysMap = {};
        var idsEnHistorial = {};
        for(var i=0; i<partidos.length; i++) {
            if(idsEnHistorial[partidos[i].id_partido]) continue;
            idsEnHistorial[partidos[i].id_partido] = true;
"""

js = js.replace(old_hist_loop, new_hist_loop)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(js)
    print("Patched history loop and permitido!")

