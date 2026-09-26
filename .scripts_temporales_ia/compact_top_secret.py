import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the layout of the Team cards to be compact
old_card = r'<div class="vcv-card-v2" style="margin-bottom:20px; border-left:4px solid var\(--vcv-dorado\);">\s*<h4 style="color:var\(--vcv-morado\); margin-bottom:5px; font-weight:bold;">\$\{eq\}</h4>\s*<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">\s*<span style="background:rgba\(16, 185, 129, 0\.15\); color:#10b981; padding:4px 10px; border-radius:8px; border:1px solid rgba\(16, 185, 129, 0\.3\); font-weight:bold; font-size:0\.85rem;">Llevan: \$\{ptsActuales\} puntos reales</span>\s*</div>\s*\$\{miCajonHTML\}\s*<details>'

new_card = r"""<div class="vcv-card-v2" style="margin-bottom:10px; padding: 12px; border-left:4px solid var(--vcv-dorado);">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <h4 style="color:var(--text-main); margin:0; font-weight:800; font-size:1.1rem; letter-spacing:-0.5px;">${eq}</h4>
                            <span style="background:rgba(16, 185, 129, 0.15); color:#10b981; padding:2px 8px; border-radius:6px; border:1px solid rgba(16, 185, 129, 0.3); font-weight:bold; font-size:0.75rem;">Llevan: ${ptsActuales} pts</span>
                        </div>
                        
                        ${miCajonHTML}

                        <details>"""

text = re.sub(old_card, new_card, text)

# 2. Update miCajonHTML styling for open state (the input box)
old_open = r'<div style="background:var\(--bg-card-alt\); padding:15px; border-radius:12px; border:1px solid var\(--border-color\); margin-bottom:15px;">\s*<label style="font-weight:bold; color:var\(--text-muted\); font-size:0\.85rem; display:block; margin-bottom:6px;">Tu predicción final:</label>\s*<div style="display:flex; gap:10px;">\s*<input type="number" id="pt_\$\{eq\}" class="form-control" placeholder="Ej: 45" value="\$\{misPts\}">\s*</div>\s*</div>'

new_open = r"""<div style="background:var(--bg-card-alt); padding:10px; border-radius:10px; border:1px solid var(--border-color); margin-bottom:10px; display:flex; align-items:center; justify-content:space-between;">
                            <label style="font-weight:700; color:var(--text-muted); font-size:0.75rem; margin:0; text-transform:uppercase;">Tu predicción:</label>
                            <div class="stepper-container-v2" style="width: 140px; background:var(--bg-input);">
                                <button type="button" class="btn-step-v2" style="width:30px; height:30px; border-radius:6px;" onclick="document.getElementById('pt_${eq}').stepDown()">-</button>
                                <div class="stepper-value-v2" style="flex:1; min-width:auto;">
                                    <input type="number" id="pt_${eq}" placeholder="0" value="${misPts}" style="background:transparent; border:none; text-align:center; font-size:1.1rem; font-weight:900; color:var(--secondary-color); width:100%; outline:none; -moz-appearance:textfield; margin:0; padding:0; height:30px;">
                                </div>
                                <button type="button" class="btn-step-v2" style="width:30px; height:30px; border-radius:6px;" onclick="document.getElementById('pt_${eq}').stepUp()">+</button>
                            </div>
                        </div>"""
text = re.sub(old_open, new_open, text)

# 3. Update miCajonHTML styling for closed state
old_closed = r'<div style="background:var\(--bg-card-alt\); padding:15px; border-radius:12px; border:1px solid var\(--border-color\); margin-bottom:15px;">\s*<label style="font-weight:bold; color:var\(--text-muted\); font-size:0\.85rem; display:block; margin-bottom:6px;">Tu predicción final:</label>\s*<div style="font-size:1\.2rem; font-weight:bold; color:var\(--vcv-morado\);">\$\{textoMiPrediccion\}</div>\s*</div>'

new_closed = r"""<div style="background:var(--bg-card-alt); padding:10px; border-radius:10px; border:1px solid var(--border-color); margin-bottom:10px; display:flex; align-items:center; justify-content:space-between;">
                            <label style="font-weight:700; color:var(--text-muted); font-size:0.75rem; margin:0; text-transform:uppercase;">Tu predicción:</label>
                            <div style="font-size:1.1rem; font-weight:900; color:var(--secondary-color);">${textoMiPrediccion}</div>
                        </div>"""

text = re.sub(old_closed, new_closed, text)

# 4. Hide spin buttons for inputs globally inside style block (if not already there)
if 'input[type=number]::-webkit-inner-spin-button' not in text:
    spin_css = """
    input[type="number"]::-webkit-outer-spin-button,
    input[type="number"]::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    input[type="number"] {
        -moz-appearance: textfield;
    }
    """
    # Insert it right before </style>
    text = re.sub(r'</style>', spin_css + '\n    </style>', text, count=1)


# 5. Fix summary padding slightly
old_summary = r'<summary style="font-weight:bold; color:var\(--vcv-morado\); cursor:pointer; outline:none;">👀 Ver predicciones de los demás</summary>'
new_summary = r'<summary style="font-weight:700; font-size:0.85rem; color:var(--text-muted); cursor:pointer; outline:none;">👀 Ver predicciones del resto</summary>'
text = re.sub(old_summary, new_summary, text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated compactness and steppers")
