import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix oDiff calculation in second block
old_diff_calc2 = r"""var setsParciales = oRes.parciales.split(",");
                    for(var sp=0; sp<setsParciales.length; sp++){
                       var nums = setsParciales[sp].split("-");
                       if(nums.length==2) oDiff += (parseInt(nums[0]) - parseInt(nums[1]));
                    }"""
new_diff_calc2 = r"""var setsParciales = oRes.parciales.split(",");
                    if (setsParciales.length === 1 && !oRes.parciales.includes("-") && !isNaN(parseInt(oRes.parciales))) {
                        oDiff = parseInt(oRes.parciales);
                    } else {
                        for(var sp=0; sp<setsParciales.length; sp++){
                            var nums = setsParciales[sp].split("-");
                            if(nums.length==2) oDiff += (parseInt(nums[0]) - parseInt(nums[1]));
                        }
                    }"""

if old_diff_calc2 in text:
    text = text.replace(old_diff_calc2, new_diff_calc2)
    print("Fixed oDiff in block 2")

# Fix points additivity in second block
old_pts_add = r"""if(uPred.sets === oRes.sets) { ptsGanados += pS; motivos.push("Sets exactos (+" + pS + ")"); }
                    else if (uLocalWin === oLocalWin) { ptsGanados += pG; motivos.push("Acertar ganador (+" + pG + ")"); }"""
new_pts_add = r"""if (uLocalWin === oLocalWin) { ptsGanados += pG; motivos.push("Ganador (+" + pG + ")"); }
                    if (uPred.sets === oRes.sets) { ptsGanados += pS; motivos.push("Sets exactos (+" + pS + ")"); }"""

if old_pts_add in text:
    text = text.replace(old_pts_add, new_pts_add)
    print("Fixed additivity in block 2")
    
# Fix distance in block 2
old_dist_2 = r"""var distancia = Math.abs(oDiff - uDiff);
                    if(distancia === 0) { ptsGanados += pDE; motivos.push("Dif. exacta (+" + pDE + ")"); }
                    else if(distancia <= 5) { ptsGanados += pD5; motivos.push("Dif. aproximada (+" + ptsDiff5 + ")"); }"""
new_dist_2 = r"""var distancia = Math.abs(oDiff - uDiff);
                    if(distancia === 0) { 
                        ptsGanados += pDE; 
                        motivos.push("Dif. exacta (+" + pDE + ")"); 
                    } else if(maxDist > 0 && distancia < maxDist) { 
                        var porcentaje = (maxDist - distancia) / maxDist;
                        var ptsDiferencia = Math.round(pDE * porcentaje);
                        ptsGanados += ptsDiferencia;
                        motivos.push("Dif. acercada [" + distancia + "] (+" + ptsDiferencia + ")");
                    }"""

if old_dist_2 in text:
    text = text.replace(old_dist_2, new_dist_2)
    print("Fixed distance in block 2")

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done fixing block 2!")
