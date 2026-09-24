import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    js = f.read()

target = 'if(uPred.sets === oRes.sets) { ptsGanados += ptsSets; motivos.push("Sets exactos (+" + ptsSets + ")"); }\r\n                    else if (uLocalWin === oLocalWin) { ptsGanados += ptsGanador; motivos.push("Acertar ganador (+" + ptsGanador + ")"); }\r\n\r\n                    var distancia = Math.abs(oDiff - uDiff);\r\n                    if(distancia === 0) { ptsGanados += ptsDiffExacta; motivos.push("Dif. exacta (+" + ptsDiffExacta + ")"); }\r\n                    else if(distancia <= 5) { ptsGanados += ptsDiff5; motivos.push("Dif. cercana (+" + ptsDiff5 + ")"); }'

new_hist = """var esDerby = misPermisos[p.equipo_local] === true && misPermisos[p.rival] === true;
                    var pS = esDerby ? ptsSets * 2 : ptsSets;
                    var pG = esDerby ? ptsGanador * 2 : ptsGanador;
                    var pDE = esDerby ? ptsDiffExacta * 2 : ptsDiffExacta;
                    var pD5 = esDerby ? ptsDiff5 * 2 : ptsDiff5;

                    if(esDerby) motivos.push("🔥 DERBY (x2)");

                    if(uPred.sets === oRes.sets) { ptsGanados += pS; motivos.push("Sets exactos (+" + pS + ")"); }
                    else if (uLocalWin === oLocalWin) { ptsGanados += pG; motivos.push("Acertar ganador (+" + pG + ")"); }

                    var distancia = Math.abs(oDiff - uDiff);
                    if(distancia === 0) { ptsGanados += pDE; motivos.push("Dif. exacta (+" + pDE + ")"); }
                    else if(distancia <= 5) { ptsGanados += pD5; motivos.push("Dif. cercana (+" + pD5 + ")"); }"""

if target in js:
    js = js.replace(target, new_hist)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched get_history!")
else:
    print("Failed finding target with \\r\\n!")

