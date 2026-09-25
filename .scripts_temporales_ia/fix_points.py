import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix 1: Parsing of direct oDiff (if user enters '15' instead of '25-20,...')
old_diff_calc = r"""var setsParciales = oRes.parciales.split(",");
                for(var sp=0; sp<setsParciales.length; sp++){
                    var nums = setsParciales[sp].split("-");
                    if(nums.length==2) oDiff += (parseInt(nums[0]) - parseInt(nums[1]));
                }"""
new_diff_calc = r"""var setsParciales = oRes.parciales.split(",");
                if (setsParciales.length === 1 && !oRes.parciales.includes("-") && !isNaN(parseInt(oRes.parciales))) {
                    oDiff = parseInt(oRes.parciales);
                } else {
                    for(var sp=0; sp<setsParciales.length; sp++){
                        var nums = setsParciales[sp].split("-");
                        if(nums.length==2) oDiff += (parseInt(nums[0]) - parseInt(nums[1]));
                    }
                }"""
text = text.replace(old_diff_calc, new_diff_calc)


# Fix 2: Additive points for Sets AND Winner (first occurrence)
old_pts_1 = r"""var ptsGanados = 0;
                if(uPred.sets === oRes.sets) { ptsGanados += pS; }
                else if (uLocalWin === oLocalWin) { ptsGanados += pG; }"""
new_pts_1 = r"""var ptsGanados = 0;
                if (uLocalWin === oLocalWin) { ptsGanados += pG; }
                if (uPred.sets === oRes.sets) { ptsGanados += pS; }"""
text = text.replace(old_pts_1, new_pts_1)

# Fix 3: Additive points for Sets AND Winner (second occurrence with motivos)
old_pts_2 = r"""if(uPred.sets === oRes.sets) { ptsGanados += pS; motivos.push("Sets exactos (+" + pS + ")"); }
                    else if (uLocalWin === oLocalWin) { ptsGanados += pG; motivos.push("Ganador acertado (+" + pG + ")"); }"""
new_pts_2 = r"""if (uLocalWin === oLocalWin) { ptsGanados += pG; motivos.push("Ganador (+" + pG + ")"); }
                    if (uPred.sets === oRes.sets) { ptsGanados += pS; motivos.push("Sets exactos (+" + pS + ")"); }"""
text = text.replace(old_pts_2, new_pts_2)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Código.js points logic fixed!")
