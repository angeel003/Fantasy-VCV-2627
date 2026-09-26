import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the changing points logic
target_js1 = "let current = parseInt(hiddenInput.value) || 14;"
new_js1 = """let current = parseInt(hiddenInput.value);
          if (isNaN(current)) current = 14;"""
if target_js1 in text:
    text = text.replace(target_js1, new_js1)
    print("Fixed parseInt logic")
else:
    print("parseInt target not found")

# Fix HTML layout logic
# 1. Search for `let ptsText = "", formStr = "";` to add the HTML generation
target_js2 = """let ptsText = "", formStr = "";
                if (data.predicciones_usuario && data.predicciones_usuario[eq.id_partido]) {"""
new_js2 = """let ptsText = "", formStr = "";
                let savedSummaryHtml = "";
                if (data.predicciones_usuario && data.predicciones_usuario[eq.id_partido]) {"""

text = text.replace(target_js2, new_js2)

# 2. Search for the end of the `if` block to insert the summary building logic
target_js3 = """if(pPts == 0) formStr = `(0 pts)`;
                }
                let valJornada = String(eq.jornada_eq || "").trim();"""
new_js3 = """if(pPts == 0) formStr = `(0 pts)`;
                    
                    let localTeamName = (eq.ubicacion === 'LOCAL') ? eq.equipo_local : eq.rival;
                    let visitTeamName = (eq.ubicacion === 'LOCAL') ? eq.rival : eq.equipo_local;
                    let formattedSets = pSets.replace('-', ' - ');
                    
                    savedSummaryHtml = `<div style="background: var(--bg-card-alt); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: var(--text-muted); margin-top: 15px;">
                                          <i data-lucide="check-circle" style="width: 16px; height: 16px; color: var(--success);"></i>
                                          <span>Configurada: <strong style="color: var(--text-main); font-weight:800;">${localTeamName} ${formattedSets} ${visitTeamName} ${formStr}</strong></span>
                                        </div>`;
                }
                let valJornada = String(eq.jornada_eq || "").trim();"""

text = text.replace(target_js3, new_js3)

# 3. Insert `savedSummaryHtml` before the save button
target_js4 = """                            <button type="button" id="btn-save-${eq.id_partido}" onclick="handleSaveOrModifyV2('${eq.id_partido}')" style="width:100%; margin-top:15px; padding:12px; border-radius:10px; ${isPredicted ? "background:transparent; color:var(--text-muted); font-weight:800; border:1px solid var(--border-color);" : "background:var(--secondary-color); color:#000; font-weight:800; border:none;"} cursor:pointer; transition: all 0.2s;">
                                ${isPredicted ? "Modificar Predicción" : "Guardar Predicción"}
                            </button>`}
                            
                            ${destacadoHtml}"""

new_js4 = """                            ${savedSummaryHtml}
                            <button type="button" id="btn-save-${eq.id_partido}" onclick="handleSaveOrModifyV2('${eq.id_partido}')" style="width:100%; margin-top:10px; padding:12px; border-radius:10px; ${isPredicted ? "background:transparent; color:var(--text-muted); font-weight:800; border:1px solid var(--border-color);" : "background:var(--secondary-color); color:#000; font-weight:800; border:none;"} cursor:pointer; transition: all 0.2s;">
                                ${isPredicted ? "Modificar Predicción" : "Guardar Predicción"}
                            </button>`}
                            
                            ${destacadoHtml}"""

text = text.replace(target_js4, new_js4)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("HTML template logic modified")
