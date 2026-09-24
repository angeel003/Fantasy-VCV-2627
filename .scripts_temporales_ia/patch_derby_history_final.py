import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = 'if(uPred.sets === oRes.sets) { ptsGanados += ptsSets; motivos.push("Sets exactos (+" + ptsSets + ")"); }\n                    else if (uLocalWin === oLocalWin) { ptsGanados += ptsGanador; motivos.push("Acertar ganador (+" + ptsGanador + ")"); }\n\n                    var distancia = Math.abs(oDiff - uDiff);\n                    if(distancia === 0) { ptsGanados += ptsDiffExacta; motivos.push("Dif. exacta (+" + ptsDiffExacta + ")"); }\n                    else if(distancia <= 5) { ptsGanados += ptsDiff5; motivos.push("Dif. cercana (+" + ptsDiff5 + ")"); }'

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

# Normalise newlines
js_lines = js.replace('\r\n', '\n')

if target in js_lines:
    js_new = js_lines.replace(target, new_hist)
    with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
        f.write(js_new)
    print('Patched get_history successfully!')
else:
    print('Still not found!')

