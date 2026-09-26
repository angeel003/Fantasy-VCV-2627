import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                .then(pData => {
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
                                let visitAb = card.querySelectorAll('.team-name-v2')[1]?.innerText || "";"""

new = """                .then(pData => {
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
                                let localAbNodes = card.querySelectorAll('.team-name-v2');
                                let localAb = localAbNodes.length > 0 ? localAbNodes[0].innerText : "";
                                let visitAb = localAbNodes.length > 1 ? localAbNodes[1].innerText : "";"""

if target in text:
    text = text.replace(target, new)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed optional chaining")
else:
    print("Target not found")
