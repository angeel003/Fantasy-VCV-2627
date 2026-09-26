import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Timer fix. We want to remove the old timer and put it in the header.
old_timer = r'<div class="reloj-partido" data-ts="\$\{eq\.timestamp\}" data-eq="\$\{eq\.id_partido\}" style="font-size:0\.75rem; font-weight:bold; padding:4px 8px; background:rgba\(212, 175, 55, 0\.1\); color:var\(--secondary-color\); border: 1px solid var\(--border-glow\); border-radius:4px; display:inline-block; margin-bottom:12px;">Calculando tiempo...</div>'
text = re.sub(old_timer, '', text)

old_header = r"""<div class="match-header-strip-v2">
                                <span style="color: \$\{eq\.es_derby \? 'var\(--text-gold\)' : 'var\(--secondary-color\)'\}; font-weight: 800;">
                                  \$\{eq\.categoria\.toUpperCase\(\)\} \$\{eq\.es_derby \? ' DERBY' : ''\}
                                </span>"""

new_header = r"""<div class="match-header-strip-v2">
                                <div style="display:flex; align-items:center; gap:8px;">
                                    <span style="color: ${eq.es_derby ? 'var(--text-gold)' : 'var(--secondary-color)'}; font-weight: 800;">
                                      ${eq.categoria.toUpperCase()} ${eq.es_derby ? ' DERBY' : ''}
                                    </span>
                                    <div class="reloj-partido" data-ts="${eq.timestamp}" data-eq="${eq.id_partido}" style="font-size:0.65rem; font-weight:bold; padding:2px 6px; background:rgba(212, 175, 55, 0.1); color:var(--secondary-color); border: 1px solid var(--border-glow); border-radius:4px; display:inline-block;">Calculando tiempo...</div>
                                </div>"""

text = re.sub(old_header, new_header, text)

# 2. CERRADO style fix.
# We replace `if (eq.estado === "ABIERTO") {` with `if (eq.estado === "ABIERTO" || eq.estado === "CERRADO") {`
# But only for the one in `btnLogin`!
# Let's do it safely:
text = text.replace('if (eq.estado === "ABIERTO") {', 'if (eq.estado === "ABIERTO" || eq.estado === "CERRADO") {')

# Remove old CERRADO block safely.
text = re.sub(r'\} else if \(eq\.estado === "CERRADO"\) \{.*?</div>`;\s*\}', '', text, flags=re.DOTALL)

# 3. Add points text and hide inputs if CERRADO
# In `btnLogin` loop:
old_inputs = r'<!-- HIDDEN INPUTS -->'
new_inputs = r"""${eq.estado === "CERRADO" ? `<div style="text-align:center; margin-top:15px; padding:15px; background:var(--bg-card-alt); border-radius:12px; border:1px solid var(--border-color);"><div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px;">RESULTADO OFICIAL</div><div style="font-size: 1.25rem; font-weight: 900; color: var(--text-main);">${eq.oficial_sets || 'Sin resultado'}</div><div style="font-size: 0.85rem; color: var(--text-muted);">${eq.oficial_parciales || ''}</div></div>` : `
                            <!-- PUNTOS TEXT -->
                            <div style="font-size: 0.7rem; color: var(--text-muted); text-align: center; margin-bottom: 12px; font-weight: bold;">
                                Sets Exactos: <span style="color:var(--success);">+${data.reglas?.puntos_sets_exactos || 80} pts</span> | 
                                Diferencia: <span style="color:var(--success);">+${data.reglas?.puntos_diferencia_exacta || 100} pts</span>
                            </div>
                            <!-- HIDDEN INPUTS -->`}"""
text = text.replace(old_inputs, new_inputs)

text = re.sub(r'<button type="button" id="btn-save-\$\{eq\.id_partido\}"', r'${eq.estado === "CERRADO" ? "" : `<button type="button" id="btn-save-${eq.id_partido}"', text)
text = re.sub(r'Guardar Predicción\s*</button>', r'Guardar Predicción\n                            </button>`}', text)

# 4. Error Message Color Fix
text = text.replace('<div id="loginMessage" class="alert-box" style="margin-top:10px; display:none;"></div>', 
                    '<div id="loginMessage" class="alert-box" style="margin-top:10px; display:none; background-color:#ff4444; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:bold;"></div>')


# 5. Fix Guest mode text
text = text.replace('Entrar como Invitado', 'Entrar como Invitado (Solo Lectura)')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done replacements.")
