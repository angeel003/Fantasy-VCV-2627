import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    js = f.read()

old_guest = """        var idsEnInvitado = {};
        for(var p=0; p<partidos.length; p++) {
            if(misPermisosInvitado[partidos[p].equipo_local] === true) {
                var pId = partidos[p].id_partido;
                if(!idsEnInvitado[pId]) {
                    carteleraInvitado.push(partidos[p]);
                    idsEnInvitado[pId] = partidos[p];
                } else {
                    idsEnInvitado[pId].es_derby = true;
                }
            }
        }"""

new_guest = """        var idsEnInvitado = {};
        for(var p=0; p<partidos.length; p++) {
            var esLoc = misPermisosInvitado[partidos[p].equipo_local] === true;
            var esRiv = misPermisosInvitado[partidos[p].rival] === true;
            if(esLoc || esRiv) {
                var pId = partidos[p].id_partido;
                var pCopy = JSON.parse(JSON.stringify(partidos[p]));
                if(esLoc && esRiv) pCopy.es_derby = true;
                
                if(!idsEnInvitado[pId]) {
                    carteleraInvitado.push(pCopy);
                    idsEnInvitado[pId] = pCopy;
                } else {
                    if(esLoc && esRiv) idsEnInvitado[pId].es_derby = true;
                }
            }
        }"""

js = js.replace(old_guest, new_guest)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(js)
    print("Patched guest resilient deduplication")

