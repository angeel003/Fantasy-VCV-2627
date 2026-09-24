import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    js = f.read()

old_dedup = """        for(var i=0; i<partidos.length; i++) { 
            if(partidos[i].permitido) {
                var pId = partidos[i].id_partido;
                
                if(!idsEnTodos[pId]) {
                    todosPartidos.push(partidos[i]);
                    idsEnTodos[pId] = partidos[i];
                } else {
                    idsEnTodos[pId].es_derby = true;
                }
                
                if(partidos[i].visibilidad === "MOSTRAR") {
                    if(!idsEnCartelera[pId]) {
                        cartelera.push(partidos[i]);
                        idsEnCartelera[pId] = partidos[i];
                    } else {
                        idsEnCartelera[pId].es_derby = true;
                    }
                }
            } 
        }"""

new_dedup = """        for(var i=0; i<partidos.length; i++) { 
            // We want to allow the match if they follow eqLoc OR rival.
            // But since 'permitido' is only checking eqLoc right now, we should check both explicitly here!
            var esLoc = misPermisos[partidos[i].equipo_local] === true;
            var esRiv = misPermisos[partidos[i].rival] === true;
            
            if(esLoc || esRiv) {
                var pId = partidos[i].id_partido;
                var pCopy = JSON.parse(JSON.stringify(partidos[i]));
                
                // Set the UI names properly. If they only follow the away team, make the away team local in their UI?
                // No, the UI is fine as long as they see the match.
                // The crucial part: Mark as derby if they follow BOTH teams!
                if(esLoc && esRiv) {
                    pCopy.es_derby = true;
                }
                
                if(!idsEnTodos[pId]) {
                    todosPartidos.push(pCopy);
                    idsEnTodos[pId] = pCopy;
                } else {
                    if(esLoc && esRiv) idsEnTodos[pId].es_derby = true;
                }
                
                if(pCopy.visibilidad === "MOSTRAR") {
                    if(!idsEnCartelera[pId]) {
                        cartelera.push(pCopy);
                        idsEnCartelera[pId] = pCopy;
                    } else {
                        if(esLoc && esRiv) idsEnCartelera[pId].es_derby = true;
                    }
                }
            } 
        }"""

js = js.replace(old_dedup, new_dedup)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(js)
    print("Patched deduplication and derby logic to be resilient to 1 or 2 rows.")

