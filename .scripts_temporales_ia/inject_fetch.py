import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """if(window.initCalendar) window.initCalendar();
            
            if(data.reglas) {"""

new = """if(window.initCalendar) window.initCalendar();
            
            // BACKGROUND FETCH PREDICCIONES
            setTimeout(() => {
                fetchSeguro(scriptURL, { 
                    method: 'POST', 
                    body: JSON.stringify({ action: 'get_mis_predicciones', usuario: currentUser, password: currentPassword }), 
                    headers: { 'Content-Type': 'text/plain;charset=utf-8' }
                })
                .then(res => res.json())
                .then(pData => {
                    if (pData.status === 'success' && pData.predicciones) {
                        if(!window.appData) window.appData = {};
                        window.appData.predicciones_usuario = pData.predicciones;
                        
                        for (let idPart in pData.predicciones) {
                            let pred = pData.predicciones[idPart];
                            let summaryTextDiv = document.getElementById('summary-text-' + idPart);
                            let summaryDiv = document.getElementById('summary-v2-' + idPart);
                            let card = document.getElementById('card-v2-' + idPart);
                            let btnSave = document.getElementById('btn-save-' + idPart);
                            
                            if (summaryTextDiv && card) {
                                let localAb = card.querySelectorAll('.team-name-v2')[0]?.innerText || "";
                                let visitAb = card.querySelectorAll('.team-name-v2')[1]?.innerText || "";
                                
                                let pSig = pred.signo || "";
                                let pPts = pred.puntos || "";
                                let pSets = pred.sets || "";
                                
                                let winnerName = "";
                                if (pSig.toLowerCase().includes('a favor')) winnerName = localAb;
                                else if (pSig.toLowerCase().includes('en contra')) winnerName = visitAb;
                                
                                let formStr = winnerName ? `(+${pPts} pts para ${winnerName})` : `(${pPts} pts)`;
                                if(pPts == 0) formStr = `(0 pts)`;
                                let formattedSets = pSets.replace('-', ' - ');
                                
                                summaryTextDiv.innerHTML = `<div style="background: var(--bg-card-alt); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: var(--text-muted); text-align: left;"><i data-lucide="check-circle" style="width: 16px; height: 16px; color: var(--success); flex-shrink: 0;"></i><span>Guardada: <strong style="color: var(--text-main); font-weight:800;">${localAb} ${formattedSets} ${visitAb} ${formStr}</strong></span></div>`;
                                
                                if(summaryDiv) summaryDiv.style.display = 'block';
                                card.classList.add('collapsed');
                                let inputsBox = document.getElementById('inputs_eq_' + idPart);
                                if(inputsBox) inputsBox.style.display = 'none';
                                
                                if(btnSave) {
                                    btnSave.innerText = 'Modificar Predicción';
                                    btnSave.style.background = 'transparent';
                                    btnSave.style.border = '1px solid var(--border-color)';
                                    btnSave.style.color = 'var(--text-muted)';
                                }
                                
                                // Update hidden inputs
                                let inpSets = document.getElementById(`e${idPart}_sets`);
                                let inpPts = document.getElementById(`e${idPart}_puntos`);
                                let inpSig = document.getElementById(`e${idPart}_signo`);
                                if(inpSets) inpSets.value = pSets;
                                if(inpPts) inpPts.value = pPts;
                                if(inpSig) inpSig.value = pSig;
                                
                                // Update buttons UI internally
                                if(pSig.toLowerCase().includes('a favor')) {
                                    let b = document.getElementById(`signo-plus-v2-${idPart}`); if(b) b.classList.add('selected');
                                } else if(pSig.toLowerCase().includes('en contra')) {
                                    let b = document.getElementById(`signo-minus-v2-${idPart}`); if(b) b.classList.add('selected');
                                }
                                if(pSets) {
                                    document.querySelectorAll(`#inputs_eq_${idPart} .set-option-btn-v2`).forEach(b => {
                                        if(b.innerText.trim() === pSets) b.classList.add('selected');
                                    });
                                }
                                let valDisplay = document.getElementById(`val-puntos-v2-${idPart}`);
                                if(valDisplay) valDisplay.innerText = pPts;
                                
                                if(window.lucide) lucide.createIcons();
                            }
                        }
                    }
                }).catch(e => console.log('Error silente al cargar preds', e));
            }, 1500); // 1.5s delay to let UI render and settle

            if(data.reglas) {"""

if target in text:
    text = text.replace(target, new)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Injected background fetch in v2.html")
else:
    print("Target not found")
