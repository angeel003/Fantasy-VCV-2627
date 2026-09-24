import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    js = f.read()

old_hist_regex = r'if\(uPred\.sets === oRes\.sets\) \{ ptsGanados \+= ptsSets.*?else if\(distancia <= 5\) \{ ptsGanados \+= ptsDiff5; motivos\.push\("Dif\. cercana \(\+" \+ ptsDiff5 \+ "\)"\); \}'

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

js_new = re.sub(old_hist_regex, new_hist, js, flags=re.DOTALL)

if js_new != js:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(js_new)
    print("Patched get_history!")
else:
    print("Regex failed!")

