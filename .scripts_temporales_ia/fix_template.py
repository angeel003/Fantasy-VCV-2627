import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_block = """                let isPredicted = false;
                let pSets = "", pPts = "", pSig = "";
                let ptsText = "", formStr = "";
                if (prediccionesList[eq.id_partido]) {
                    isPredicted = true;
                    pSets = prediccionesList[eq.id_partido].sets || "";
                    pPts = prediccionesList[eq.id_partido].puntos || "";
                    pSig = prediccionesList[eq.id_partido].signo || "";
                    ptsText = pSig === 'A favor (+)' ? 'a favor' : (pSig === 'En contra (-)' ? 'en contra' : '');
                    formStr = ptsText ? `(+${pPts} pts ${ptsText})` : `(${pPts} pts)`;
                    if(pPts == 0) formStr = `(0 pts)`;
                }"""

new_block = """                let isPredicted = false;
                let pSets = "", pPts = "", pSig = "";
                let ptsText = "", formStr = "";
                if (data.predicciones_usuario && data.predicciones_usuario[eq.id_partido]) {
                    isPredicted = true;
                    pSets = data.predicciones_usuario[eq.id_partido].sets || "";
                    pPts = data.predicciones_usuario[eq.id_partido].puntos || "";
                    pSig = data.predicciones_usuario[eq.id_partido].signo || "";
                    ptsText = pSig === 'A favor (+)' ? 'a favor' : (pSig === 'En contra (-)' ? 'en contra' : '');
                    formStr = ptsText ? `(+${pPts} pts ${ptsText})` : `(${pPts} pts)`;
                    if(pPts == 0) formStr = `(0 pts)`;
                }"""

if old_block in text:
    text = text.replace(old_block, new_block)
else:
    print("WARNING: Old block not found!")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Template safe fix applied")
