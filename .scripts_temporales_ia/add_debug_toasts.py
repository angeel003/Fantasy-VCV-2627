import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                .then(pData => {
                    if (pData.status === 'success' && pData.predicciones) {
                        if(!window.appData) window.appData = {};"""

new = """                .then(pData => {
                    if (pData.status === 'success' && pData.predicciones) {
                        let countPreds = Object.keys(pData.predicciones).length;
                        if(typeof mostrarToast === 'function') mostrarToast(`Cargadas ${countPreds} predicciones guardadas`);
                        if(!window.appData) window.appData = {};"""

if target in text:
    text = text.replace(target, new)
    
    # Also add a toast in the catch block to debug if it fails!
    target2 = """).catch(e => console.log('Error silente al cargar preds', e));"""
    new2 = """).catch(e => { console.log('Error silente al cargar preds', e); if(typeof mostrarToast === 'function') mostrarToast('Error cargando predicciones: ' + e.message); });"""
    text = text.replace(target2, new2)
    
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added debug toasts")
else:
    print("Target not found")
