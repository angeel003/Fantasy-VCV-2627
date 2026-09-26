import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

new_dist = r"""var distancia = Math.abs(oDiff - uDiff);
                    if(distancia === 0) { 
                        ptsGanados += pDE; 
                        motivos.push("Dif. exacta (+" + pDE + ")"); 
                    } else if(maxDist > 0 && distancia < maxDist) { 
                        var porcentaje = (maxDist - distancia) / maxDist;
                        var ptsDiferencia = Math.round(pDE * porcentaje);
                        ptsGanados += ptsDiferencia;
                        motivos.push("Dif. acercada [" + distancia + "] (+" + ptsDiferencia + ")");
                    }"""

pattern = r'var distancia = Math\.abs\(oDiff - uDiff\);\s*if\(distancia === 0\) \{ ptsGanados \+= pDE; motivos\.push\("Dif\. exacta \(\+" \+ pDE \+ "\)"\); \}\s*else if\(distancia <= 5\) \{ ptsGanados \+= pD5; motivos\.push\("Dif\. aproximada \(\+" \+ ptsDiff5 \+ "\)"\); \}'

if re.search(pattern, text):
    text = re.sub(pattern, new_dist, text)
    with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Success replacing block 2 distance!")
else:
    print("Regex still didn't match Block 2 distance!")
