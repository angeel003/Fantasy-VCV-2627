import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    js = f.read()

old_permitido = """    for(var p=0; p<partidos.length; p++) {
        var eqLoc = partidos[p].equipo_local;
        partidos[p].permitido = (misPermisos[eqLoc] === true);
    }"""

new_permitido = """    // Marcar partidos permitidos y Derbys
    var idsVistos = {};
    for(var p=0; p<partidos.length; p++) {
        var eqLoc = partidos[p].equipo_local;
        var eqRival = partidos[p].rival;
        var esLoc = (misPermisos[eqLoc] === true);
        var esRiv = (misPermisos[eqRival] === true);
        
        if (esLoc || esRiv) {
            partidos[p].permitido = true;
            if (esLoc && esRiv) { partidos[p].es_derby = true; }
            
            // Deduplicar si el admin mete dos filas (una para cada equipo)
            var id = partidos[p].id_partido;
            if(idsVistos[id]) {
                partidos[p].permitido = false; // ocultar el duplicado
            } else {
                idsVistos[id] = true;
            }
        } else {
            partidos[p].permitido = false;
        }
    }"""

js = js.replace(old_permitido, new_permitido)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(js)
    print("Patched permitido for Derbys")

