import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                let isPredicted = false;
                let pSets = "", pPts = "", pSig = "";
                let ptsText = "", formStr = "";
                
                console.log('Preds para ' + eq.id_partido + ':', data.predicciones_usuario ? data.predicciones_usuario[eq.id_partido] : 'none');
                if (data.predicciones_usuario && data.predicciones_usuario[eq.id_partido]) {
                    isPredicted = true;
                    pSets = data.predicciones_usuario[eq.id_partido].sets || "";
                    pPts = data.predicciones_usuario[eq.id_partido].puntos || "";
                    pSig = data.predicciones_usuario[eq.id_partido].signo || "";
                    let savedLocalName = (eq.ubicacion === 'LOCAL') ? eq.equipo_local : eq.rival;
                    let savedVisitName = (eq.ubicacion === 'LOCAL') ? eq.rival : eq.equipo_local;
                    let winnerName = "";
                    if (pSig.toLowerCase().includes('a favor')) winnerName = savedLocalName;
                    else if (pSig.toLowerCase().includes('en contra')) winnerName = savedVisitName;
                    formStr = winnerName ? `(+${pPts} pts para ${winnerName})` : `(${pPts} pts)`;
                    if(pPts == 0) formStr = `(0 pts)`;
                    let formattedSets = pSets.replace('-', ' - ');
                    
                    
                }"""

new = """                let isPredicted = false;
                let pSets = "", pPts = "", pSig = "";
                let ptsText = "", formStr = "";
                let savedLocalName = "", savedVisitName = "", formattedSets = "";
                
                console.log('Preds para ' + eq.id_partido + ':', data.predicciones_usuario ? data.predicciones_usuario[eq.id_partido] : 'none');
                if (data.predicciones_usuario && data.predicciones_usuario[eq.id_partido]) {
                    isPredicted = true;
                    pSets = data.predicciones_usuario[eq.id_partido].sets || "";
                    pPts = data.predicciones_usuario[eq.id_partido].puntos || "";
                    pSig = data.predicciones_usuario[eq.id_partido].signo || "";
                    savedLocalName = (eq.ubicacion === 'LOCAL') ? eq.equipo_local : eq.rival;
                    savedVisitName = (eq.ubicacion === 'LOCAL') ? eq.rival : eq.equipo_local;
                    let winnerName = "";
                    if (pSig.toLowerCase().includes('a favor')) winnerName = savedLocalName;
                    else if (pSig.toLowerCase().includes('en contra')) winnerName = savedVisitName;
                    formStr = winnerName ? `(+${pPts} pts para ${winnerName})` : `(${pPts} pts)`;
                    if(pPts == 0) formStr = `(0 pts)`;
                    formattedSets = String(pSets).replace('-', ' - ');
                }"""

if target in text:
    text = text.replace(target, new)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed scope")
else:
    print("Target not found")
