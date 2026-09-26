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
text = text.replace(old_diff_calc2, new_diff_calc2)

# Fix points additivity in second block
old_pts_add = r"""if(uPred.sets === oRes.sets) { ptsGanados += pS; motivos.push("Sets exactos (+" + pS + ")"); }
                    else if (uLocalWin === oLocalWin) { ptsGanados += pG; motivos.push("Acertar ganador (+" + pG + ")"); }"""
new_pts_add = r"""if (uLocalWin === oLocalWin) { ptsGanados += pG; motivos.push("Ganador (+" + pG + ")"); }
                    if (uPred.sets === oRes.sets) { ptsGanados += pS; motivos.push("Sets exactos (+" + pS + ")"); }"""
text = text.replace(old_pts_add, new_pts_add)

# Let me check if my previous replacement of the first block had 'Acertar ganador' or 'Ganador'
# I used "Ganador (+" + pG + ")" which is perfectly fine, since in my previous replacement attempt for block 2, it actually didn't run because the old string had 'Acertar ganador' instead of 'Ganador acertado'. Let's verify that the old text had 'Acertar ganador'.

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Second block fixed!")

