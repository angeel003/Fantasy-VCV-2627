import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """<div class="summary-v2" id="summary-v2-${eq.id_partido}" style="display:none; margin-bottom: 12px;">
                                <div id="summary-text-${eq.id_partido}"></div>
                            </div>"""

new = """<div class="summary-v2" id="summary-v2-${eq.id_partido}" style="${isPredicted && eq.estado !== 'CERRADO' ? 'display:block;' : 'display:none;'} margin-bottom: 12px;">
                                <div id="summary-text-${eq.id_partido}">
                                ${isPredicted ? `<div style="background: var(--bg-card-alt); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: var(--text-muted); text-align: left;"><i data-lucide="check-circle" style="width: 16px; height: 16px; color: var(--success); flex-shrink: 0;"></i><span>Guardada: <strong style="color: var(--text-main); font-weight:800;">${savedLocalName} ${formattedSets} ${savedVisitName} ${formStr}</strong></span></div>` : ``}
                                </div>
                            </div>"""

if target in text:
    text = text.replace(target, new)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Injected into HTML directly")
else:
    print("Target not found")
