import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    js = f.read()

old_hist = """                    if(uPred.sets === oRes.sets) { ptsGanados += ptsSets; motivos.push(`Pleno Sets (+${ptsSets})`); }
                    else if (uLocalWin === oLocalWin) { ptsGanados += ptsGanador; motivos.push(`Acertó Ganador (+${ptsGanador})`); }
                    else { motivos.push(`Falló Ganador (0)`); }

                    var distancia = Math.abs(oDiff - uDiff);
                    if(distancia === 0) { ptsGanados += ptsDiffExacta; motivos.push(`Dif Exacta (+${ptsDiffExacta})`); }
                    else if(distancia <= 5) { ptsGanados += ptsDiff5; motivos.push(`Dif Cercana (+${ptsDiff5})`); }
                    else { motivos.push(`Dif Lejana (0)`); }"""

new_hist = """                    var esDerby = misPermisos[p.equipo_local] === true && misPermisos[p.rival] === true;
                    var pS = esDerby ? ptsSets * 2 : ptsSets;
                    var pG = esDerby ? ptsGanador * 2 : ptsGanador;
                    var pDE = esDerby ? ptsDiffExacta * 2 : ptsDiffExacta;
                    var pD5 = esDerby ? ptsDiff5 * 2 : ptsDiff5;

                    if(esDerby) motivos.push("🔥 DERBY (x2)");

                    if(uPred.sets === oRes.sets) { ptsGanados += pS; motivos.push(`Pleno Sets (+${pS})`); }
                    else if (uLocalWin === oLocalWin) { ptsGanados += pG; motivos.push(`Acertó Ganador (+${pG})`); }
                    else { motivos.push(`Falló Ganador (0)`); }

                    var distancia = Math.abs(oDiff - uDiff);
                    if(distancia === 0) { ptsGanados += pDE; motivos.push(`Dif Exacta (+${pDE})`); }
                    else if(distancia <= 5) { ptsGanados += pD5; motivos.push(`Dif Cercana (+${pD5})`); }
                    else { motivos.push(`Dif Lejana (0)`); }"""

js = js.replace(old_hist, new_hist)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(js)
    print("Patched get_history in Código.js")

