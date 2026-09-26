import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

# I will find the block 2 calculation and replace it carefully.
start = text.find('var distancia = Math.abs(oDiff - uDiff);')
start = text.find('var distancia = Math.abs(oDiff - uDiff);', start + 10) # second occurrence

if start != -1:
    end = text.find('ptsTotales += ptsGanados;', start)
    
    new_code = r"""var distancia = Math.abs(oDiff - uDiff);
                    if(distancia === 0) { 
                        ptsGanados += pDE; 
                        motivos.push("Dif. exacta (+" + pDE + ")"); 
                    } else if(maxDist > 0 && distancia < maxDist) { 
                        var porcentaje = (maxDist - distancia) / maxDist;
                        var ptsDiferencia = Math.round(pDE * porcentaje);
                        ptsGanados += ptsDiferencia;
                        motivos.push("Dif. acercada [" + distancia + "] (+" + ptsDiferencia + ")");
                    }

                    """
    
    text = text[:start] + new_code + text[end:]

    with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed!")
else:
    print("Second occurrence not found!")

