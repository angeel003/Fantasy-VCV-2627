import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_code_2 = r"""var distancia = Math.abs(oDiff - uDiff);
                    if(distancia === 0) { ptsGanados += pDE; motivos.push("Dif. exacta (+" + pDE + ")"); }
                    else if(distancia <= 5) { ptsGanados += pD5; motivos.push("Dif. aproximada (+" + ptsDiff5 + ")"); }"""

new_code_2 = r"""var distancia = Math.abs(oDiff - uDiff);
                    if(distancia === 0) { 
                        ptsGanados += pDE; 
                        motivos.push("Dif. exacta (+" + pDE + ")"); 
                    } else if(maxDist > 0 && distancia < maxDist) { 
                        var porcentaje = (maxDist - distancia) / maxDist;
                        var ptsDiferencia = Math.round(pDE * porcentaje);
                        ptsGanados += ptsDiferencia;
                        motivos.push("Dif. acercada [" + distancia + "] (+" + ptsDiferencia + ")");
                    }"""

text = text.replace(old_code_2, new_code_2)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Success!")

