import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the inner block dynamically.
# First, add the variables above if(uPred.sets === oRes.sets)
insert_vars = """var esDerby = misPermisos[p.equipo_local] === true && misPermisos[p.rival] === true;
                    var pS = esDerby ? ptsSets * 2 : ptsSets;
                    var pG = esDerby ? ptsGanador * 2 : ptsGanador;
                    var pDE = esDerby ? ptsDiffExacta * 2 : ptsDiffExacta;
                    var pD5 = esDerby ? ptsDiff5 * 2 : ptsDiff5;

                    if(esDerby) motivos.push("🔥 DERBY (x2)");

                    """

js = js.replace('if(uPred.sets === oRes.sets) { ptsGanados += ptsSets;', insert_vars + 'if(uPred.sets === oRes.sets) { ptsGanados += pS;')
js = js.replace('motivos.push("Sets exactos (+" + ptsSets + ")");', 'motivos.push("Sets exactos (+" + pS + ")");')
js = js.replace('{ ptsGanados += ptsGanador;', '{ ptsGanados += pG;')
js = js.replace('motivos.push("Acertar ganador (+" + ptsGanador + ")");', 'motivos.push("Acertar ganador (+" + pG + ")");')
js = js.replace('{ ptsGanados += ptsDiffExacta;', '{ ptsGanados += pDE;')
js = js.replace('motivos.push("Dif. exacta (+" + ptsDiffExacta + ")");', 'motivos.push("Dif. exacta (+" + pDE + ")");')
js = js.replace('{ ptsGanados += ptsDiff5;', '{ ptsGanados += pD5;')
js = js.replace('motivos.push("Dif. cercana (+" + ptsDiff5 + ")");', 'motivos.push("Dif. cercana (+" + pD5 + ")");')

with open(filename, 'w', encoding='utf-8') as f:
    f.write(js)
print("Patched incrementally!")

