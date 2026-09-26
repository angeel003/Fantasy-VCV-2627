import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Modify the optimistic UI update in handleSaveOrModifyV2
target_js1 = """document.getElementById('summary-text-' + idPart).innerHTML = `<span style="font-weight:normal; color:var(--text-muted);">Predicción configurada:</span><br><b style="font-size:1.1rem; color:var(--text-main);">${s}</b> <span style="color:var(--primary-color); font-weight:800;">${formStr}</span>`;"""
new_js1 = """let localAb = document.querySelector(`#card-v2-${idPart} .team-name-v2`) ? document.querySelectorAll(`#card-v2-${idPart} .team-name-v2`)[0].innerText : '';
            let visitAb = document.querySelector(`#card-v2-${idPart} .team-name-v2`) ? document.querySelectorAll(`#card-v2-${idPart} .team-name-v2`)[1].innerText : '';
            let formattedS = s.replace('-', ' - ');
            document.getElementById('summary-text-' + idPart).innerHTML = `<div style="background: var(--bg-card-alt); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: var(--text-muted); text-align: left;"><i data-lucide="check-circle" style="width: 16px; height: 16px; color: var(--success); flex-shrink: 0;"></i><span>Guardada: <strong style="color: var(--text-main); font-weight:800;">${localAb} ${formattedS} ${visitAb} ${formStr}</strong></span></div>`;
            if(window.lucide) setTimeout(() => window.lucide.createIcons(), 10);"""

if target_js1 in text:
    text = text.replace(target_js1, new_js1)
else:
    print("Not found target_js1")

# Modify the initialization of the summary block in login()
target_js2 = """summaryText.innerHTML = `<span style="font-weight:normal; color:var(--text-muted);">Predicción configurada:</span><br><b style="font-size:1.1rem; color:var(--text-main);">${preds[idPart].sets}</b> <span style="color:var(--primary-color); font-weight:800;">${fStr}</span>`;"""
new_js2 = """let cardEl = document.getElementById(`card-v2-${idPart}`);
                            let localAb = cardEl ? cardEl.querySelectorAll('.team-name-v2')[0].innerText : '';
                            let visitAb = cardEl ? cardEl.querySelectorAll('.team-name-v2')[1].innerText : '';
                            let formattedS = preds[idPart].sets.replace('-', ' - ');
                            summaryText.innerHTML = `<div style="background: var(--bg-card-alt); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: var(--text-muted); text-align: left;"><i data-lucide="check-circle" style="width: 16px; height: 16px; color: var(--success); flex-shrink: 0;"></i><span>Guardada: <strong style="color: var(--text-main); font-weight:800;">${localAb} ${formattedS} ${visitAb} ${fStr}</strong></span></div>`;"""

if target_js2 in text:
    text = text.replace(target_js2, new_js2)
else:
    print("Not found target_js2")

# Remove the old TU PREDICCION header from summary-v2 HTML
target_js3 = """<div class="summary-v2" id="summary-v2-${eq.id_partido}" style="display:none; text-align:center; padding: 15px; background:var(--bg-card-alt); border: 1px solid var(--border-color); border-radius: 12px; margin-bottom: 12px;">
                                <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px;">TU PREDICCIÓN</div>
                                <div id="summary-text-${eq.id_partido}" style="font-size: 1.1rem; font-weight: 800; color: var(--secondary-color);"></div>
                            </div>"""
new_js3 = """<div class="summary-v2" id="summary-v2-${eq.id_partido}" style="display:none; margin-bottom: 12px;">
                                <div id="summary-text-${eq.id_partido}"></div>
                            </div>"""

if target_js3 in text:
    text = text.replace(target_js3, new_js3)
else:
    print("Not found target_js3")

# Remove the duplicated savedSummaryHtml since we are now rendering it directly inside the summary-v2 which is ALWAYS above the button!
text = text.replace('${savedSummaryHtml}', '')
# Remove the declaration of savedSummaryHtml to clean up
text = re.sub(r'let savedSummaryHtml = "";', '', text)
text = re.sub(r'savedSummaryHtml = `<div style="background: var\(--bg-card-alt\).*?</div>`;', '', text, flags=re.DOTALL)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated summary UI")
