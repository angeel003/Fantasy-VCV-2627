import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix line 671: `<!-- HIDDEN INPUTS -->`}`}` -> `<!-- HIDDEN INPUTS -->`
text = re.sub(r'<!-- HIDDEN INPUTS -->`\}`\}', '<!-- HIDDEN INPUTS -->', text)

# Just in case it's different spacing
text = re.sub(r'<!-- HIDDEN INPUTS -->\s*`\s*\}\s*\}', '<!-- HIDDEN INPUTS -->', text)
text = re.sub(r'<!-- HIDDEN INPUTS -->`\}', '<!-- HIDDEN INPUTS -->', text)
text = re.sub(r'<!-- HIDDEN INPUTS -->\s*`\s*\}', '<!-- HIDDEN INPUTS -->', text)

# 2. Fix the button ternary mess at the end of the block
# Find everything from `<div class="summary-v2"` to `</button>`}`}`
# And replace the button to just be the button, ending with `\n                            `}`
button_regex = r'\$\{eq\.estado === "CERRADO" \? "" : `\$\{eq\.estado === "CERRADO" \? "" : `<button.*?</button>`\}`\}'
new_button = r"""<button type="button" id="btn-save-${eq.id_partido}" onclick="handleSaveOrModifyV2('${eq.id_partido}')" style="width:100%; margin-top:15px; padding:12px; border-radius:10px; background:var(--secondary-color); color:#000; font-weight:800; border:none; cursor:pointer; transition: all 0.2s;">
                                Guardar Predicción
                            </button>`}"""
text = re.sub(button_regex, new_button, text, flags=re.DOTALL)

# Just in case there's another variation of the nested ternary:
button_regex2 = r'\$\{eq\.estado === "CERRADO" \? "" : `<button.*?</button>`\}'
text = re.sub(button_regex2, new_button, text, flags=re.DOTALL)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed syntax mess")
