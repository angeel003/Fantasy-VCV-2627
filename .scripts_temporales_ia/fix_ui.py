import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add guiaModal at the bottom, just before </body>
guia_modal = """
<!-- MODAL GUIA -->
<div id="guiaModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:10000; align-items:center; justify-content:center; backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);">
    <div style="background:var(--bg-card); width:90%; max-width:400px; border-radius:16px; padding:24px; box-shadow:0 10px 40px rgba(0,0,0,0.5); position:relative; border: 1px solid var(--border-color);">
        <button onclick="document.getElementById('guiaModal').style.display='none'" style="position:absolute; top:12px; right:12px; background:none; border:none; color:var(--text-muted); font-size:1.8rem; cursor:pointer; line-height:1;">&times;</button>
        <h3 style="margin-top:0; margin-bottom:15px; color:var(--text-main); font-weight:800; font-family:'Space Grotesk', sans-serif; display:flex; align-items:center; gap:8px;">
            <i data-lucide="info" style="width:20px; height:20px;"></i> Sistema de Puntos
        </h3>
        <div style="background:var(--bg-input); border:1px dashed var(--border-color); border-radius:12px; padding:20px 15px; font-size: 0.9rem; color:var(--text-muted); max-height:60vh; overflow-y:auto; line-height:1.5;">
            <p style="margin-bottom: 10px;"><b>1. Pronóstico de sets:</b> Elige el resultado final del partido (ej. 3-1).</p>
            <p style="margin-bottom: 10px;"><b>2. Diferencia de puntos:</b> Es la suma total de la ventaja de puntos que consigue un equipo sumando todos los sets.</p>
            <p style="margin-bottom: 0;"><b>3. Signo:</b> Indica si esa diferencia de puntos será a favor del VCV (+) o del equipo rival (-).</p>
        </div>
        <button onclick="document.getElementById('guiaModal').style.display='none'" class="btn btn-primary btn-block mt-4" style="background:var(--primary-color); border:none; font-weight:bold; border-radius:8px;">Entendido</button>
    </div>
</div>
</body>"""
text = text.replace('</body>', guia_modal)

# 2. Delete the old <details> block
details_regex = r'<div style="background-color: #e3f2fd.*?</div>\s*</details>\s*</div>'
text = re.sub(details_regex, '', text, flags=re.DOTALL)

# 3. Add ? icon to "Pronóstico de sets" and "Diferencia de puntos" in HTML generation
sets_regex = r'<span style="font-size: 0\.75rem; color: var\(--text-muted\); font-weight: 800; text-transform: uppercase;">PRONSTICO DE SETS</span>'
sets_replacement = r'<span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 800; text-transform: uppercase; display:flex; align-items:center; justify-content:center; gap:5px;">PRONÓSTICO DE SETS <i data-lucide="help-circle" style="width:14px; height:14px; cursor:pointer; color:var(--primary-color);" onclick="document.getElementById(\'guiaModal\').style.display=\'flex\'"></i></span>'
text = re.sub(r'<span[^>]*>PRONSTICO DE SETS</span>', sets_replacement, text)

diff_replacement = r'<span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 800; text-transform: uppercase; display:flex; align-items:center; justify-content:center; gap:5px;">DIFERENCIA DE PUNTOS <i data-lucide="help-circle" style="width:14px; height:14px; cursor:pointer; color:var(--primary-color);" onclick="document.getElementById(\'guiaModal\').style.display=\'flex\'"></i></span>'
text = re.sub(r'<span[^>]*>DIFERENCIA DE PUNTOS</span>', diff_replacement, text)


# 4. Replace handleSaveOrModifyV2 with Optimistic UI version
old_handle = r'function handleSaveOrModifyV2\(idPart\).*?\n    \}'
new_handle = """function handleSaveOrModifyV2(idPart) {
        const card = document.getElementById('card-v2-' + idPart);
        const btn = document.getElementById('btn-save-' + idPart);
        const summary = document.getElementById('summary-v2-' + idPart);
        const inputs = document.getElementById('inputs_eq_' + idPart);
        const isCollapsed = card.classList.contains('collapsed');

        if (isCollapsed) {
            card.classList.remove('collapsed');
            summary.style.display = 'none';
            inputs.style.display = 'block';
            btn.innerText = 'Guardar Predicción';
            btn.style.background = 'var(--secondary-color)';
            btn.style.color = '#000';
            btn.style.border = 'none';
        } else {
            const s = document.getElementById('e' + idPart + '_sets').value;
            const p = document.getElementById('e' + idPart + '_puntos').value;
            const sig = document.getElementById('e' + idPart + '_signo').value;

            if (!s || !p || !sig) {
                alert('Faltan campos por rellenar en este partido.');
                return;
            }
            if(window.isGuestMode) { alert("Modo invitado. No puedes guardar."); return; }
            if(!window.currentUser) { alert("Tu sesión ha expirado."); window.location.reload(); return; }

            // OPTIMISTIC UI UPDATE
            const selectedSignBtn = document.querySelector(`#signo-plus-v2-${idPart}.selected`) || document.querySelector(`#signo-minus-v2-${idPart}.selected`);
            let signText = selectedSignBtn ? selectedSignBtn.innerText : (sig === 'Empate' ? 'Empate' : sig);
            if(p == 0) signText = "Empate";
            
            let ptsText = signText === 'A favor (+)' ? 'a favor' : (signText === 'En contra (-)' ? 'en contra' : '');
            let formStr = ptsText ? `(+${p} pts ${ptsText})` : `(${p} pts)`;
            if(p==0) formStr = `(0 pts)`;
            document.getElementById('summary-text-' + idPart).innerHTML = `<span style="font-weight:normal; color:var(--text-muted);">Predicción configurada:</span><br><b style="font-size:1.1rem; color:var(--text-main);">${s}</b> <span style="color:var(--primary-color); font-weight:800;">${formStr}</span>`;

            card.classList.add('collapsed');
            inputs.style.display = 'none';
            summary.style.display = 'block';
            
            const oldBtnHtml = btn.innerHTML;
            btn.innerHTML = 'Guardando... <span class="spinner-border spinner-border-sm" style="width:12px;height:12px;border-width:2px;margin-left:5px;"></span>';
            btn.style.background = 'transparent';
            btn.style.color = 'var(--text-muted)';
            btn.style.border = '1px solid var(--border-color)';
            btn.disabled = true;

            let singlePred = {};
            singlePred[idPart] = { sets: s, puntos: p, signo: sig };

            window.fetchSeguro(window.scriptURL, {
                method: 'POST',
                body: JSON.stringify({ action: 'guardar', usuario: window.currentUser, password: window.currentPassword, predicciones: singlePred }),
                headers: { 'Content-Type': 'text/plain;charset=utf-8' }
            }).then(res => res.json()).then(data => {
                if(data.status === "success") {
                    btn.disabled = false;
                    btn.innerText = 'Modificar Predicción';
                } else {
                    alert('Error al guardar: ' + data.message);
                    card.classList.remove('collapsed');
                    summary.style.display = 'none';
                    inputs.style.display = 'block';
                    btn.innerHTML = oldBtnHtml;
                    btn.style.background = 'var(--secondary-color)';
                    btn.style.color = '#000';
                    btn.style.border = 'none';
                    btn.disabled = false;
                }
            }).catch(err => {
                alert('Error de conexión.');
                card.classList.remove('collapsed');
                summary.style.display = 'none';
                inputs.style.display = 'block';
                btn.innerHTML = oldBtnHtml;
                btn.style.background = 'var(--secondary-color)';
                btn.style.color = '#000';
                btn.style.border = 'none';
                btn.disabled = false;
            });
        }
    }"""
text = re.sub(old_handle, new_handle, text, flags=re.DOTALL)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Tasks done.")
