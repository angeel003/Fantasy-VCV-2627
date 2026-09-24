import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    js = f.read()

old_guest = """        var carteleraInvitado = [];
        for(var p=0; p<partidos.length; p++) {
            if(misPermisosInvitado[partidos[p].equipo_local] === true) { carteleraInvitado.push(partidos[p]); }
        }"""

new_guest = """        var carteleraInvitado = [];
        var idsEnInvitado = {};
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

js = js.replace(old_guest, new_guest)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(js)
    print("Patched guest deduplication")

