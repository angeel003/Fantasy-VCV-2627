import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Deduplicate cartelera and add es_derby
old_cartelera = """        var cartelera = [];
        for(var p=0; p<partidos.length; p++) {
            if(misPermisos[partidos[p].equipo_local] === true) {
                cartelera.push(partidos[p]);
            }
        }"""

new_cartelera = """        var cartelera = [];
        var idsCartelera = {};
        for(var p=0; p<partidos.length; p++) {
            var esLocal = misPermisos[partidos[p].equipo_local] === true;
            var esRival = misPermisos[partidos[p].rival] === true;
            if(esLocal || esRival) {
                var id = partidos[p].id_partido;
                if(!idsCartelera[id]) {
                    var matchCopy = JSON.parse(JSON.stringify(partidos[p]));
                    if (esLocal && esRival) { matchCopy.es_derby = true; }
                    cartelera.push(matchCopy);
                    idsCartelera[id] = matchCopy;
                } else {
                    if (esLocal && esRival) { idsCartelera[id].es_derby = true; }
                }
            }
        }"""
js = js.replace(old_cartelera, new_cartelera)

# 2. Add es_derby logic in points calculation
# First, create permisosGlobalesMap before `for(var pUser in porrasMap)`
old_pUser_loop = "        for(var pUser in porrasMap) {"
new_pUser_loop = """        var permisosGlobalesMap = {};
        for (var r=1; r<dataPermisos.length; r++) {
            var usrPerm = dataPermisos[r][0];
            if (usrPerm) {
                permisosGlobalesMap[usrPerm] = {};
                for(var j=1; j<eqHeaders.length; j++) {
                    permisosGlobalesMap[usrPerm][eqHeaders[j]] = (dataPermisos[r][j] && dataPermisos[r][j].toString().toUpperCase() === "X");
                }
            }
        }

        for(var pUser in porrasMap) {"""
js = js.replace(old_pUser_loop, new_pUser_loop)

# 3. Inside the `pUser` loop, double the points if derby
old_ptsGanados = """                var ptsGanados = 0;
                if(uPred.sets === oRes.sets) { ptsGanados += ptsSets; }
                else if (uLocalWin === oLocalWin) { ptsGanados += ptsGanador; }

                var distancia = Math.abs(oDiff - uDiff);
                if(distancia === 0) { ptsGanados += ptsDiffExacta; }
                else if(distancia <= 5) { ptsGanados += ptsDiff5; }"""

new_ptsGanados = """                var esDerby = permisosGlobalesMap[pUser] && permisosGlobalesMap[pUser][partidoInfo.equipo_local] === true && permisosGlobalesMap[pUser][partidoInfo.rival] === true;
                var pS = esDerby ? ptsSets * 2 : ptsSets;
                var pG = esDerby ? ptsGanador * 2 : ptsGanador;
                var pDE = esDerby ? ptsDiffExacta * 2 : ptsDiffExacta;
                var pD5 = esDerby ? ptsDiff5 * 2 : ptsDiff5;
                
                var ptsGanados = 0;
                if(uPred.sets === oRes.sets) { ptsGanados += pS; }
                else if (uLocalWin === oLocalWin) { ptsGanados += pG; }

                var distancia = Math.abs(oDiff - uDiff);
                if(distancia === 0) { ptsGanados += pDE; }
                else if(distancia <= 5) { ptsGanados += pD5; }"""

# NOTE: Since ptsGanados logic occurs TWICE (once for rankings, once for get_history), we replace BOTH instances.
# Wait, in get_history, we don't need `permisosGlobalesMap[pUser]`. We can just use `misPermisos`!
# Let's see if the regex matches both! It doesn't, because `get_history` is slightly different.

# Replace in `login`/`get_data` rankings loop (first match)
js = js.replace(old_ptsGanados, new_ptsGanados, 1)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(js)
    print("Patched Código.js with basic Derby support.")

