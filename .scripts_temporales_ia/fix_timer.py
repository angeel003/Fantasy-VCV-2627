import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_logic = r"""const inputs = document\.getElementById\('inputs_eq_' \+ eqId\);
                    if\(inputs\) \{
                        inputs\.style\.opacity = '0\.5';
                        inputs\.style\.pointerEvents = 'none';
                    \}"""
new_logic = r"""const inputs = document.getElementById('inputs_eq_' + eqId);
                    if(inputs) {
                        inputs.innerHTML = '<div style="text-align:center; margin-top:15px; padding:12px; background:var(--bg-input); border-radius:12px; border:1px dashed var(--border-color);"><span style="font-size: 0.85rem; color: var(--text-muted); font-weight:bold;">El plazo para predecir este partido está cerrado.</span></div>';
                    }
                    const btnSave = document.getElementById('btn-save-' + eqId);
                    if (btnSave) btnSave.style.display = 'none';"""

text = re.sub(old_logic, new_logic, text)

# Just in case for the other block:
old_logic_2 = r"""} else if \(diff <= -14400000\) \{
                    applyStyle\('rgba\(255,255,255,0\.05\)', gray, " Partido Finalizado"\);"""
new_logic_2 = r"""} else if (diff <= -14400000) {
                    const inputs = document.getElementById('inputs_eq_' + eqId);
                    if(inputs) {
                        inputs.innerHTML = '<div style="text-align:center; margin-top:15px; padding:12px; background:var(--bg-input); border-radius:12px; border:1px dashed var(--border-color);"><span style="font-size: 0.85rem; color: var(--text-muted); font-weight:bold;">El plazo para predecir este partido está cerrado.</span></div>';
                    }
                    const btnSave = document.getElementById('btn-save-' + eqId);
                    if (btnSave) btnSave.style.display = 'none';
                    applyStyle('rgba(255,255,255,0.05)', gray, " Partido Finalizado");"""

text = re.sub(old_logic_2, new_logic_2, text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Timer closed logic updated.")
