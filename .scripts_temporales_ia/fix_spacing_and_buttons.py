import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix the spacing (move padding-bottom to appSection)
text = re.sub(
    r'#appSection > section \{\s*display: none;\s*padding-bottom: 80px; /\* space for bottom nav \*/\s*\}',
    r'#appSection > section {\n        display: none;\n        padding-bottom: 10px;\n    }',
    text
)

text = re.sub(
    r'#appSection \{\s*padding-top: 60px; /\* space for header \*/\s*\}',
    r'#appSection {\n        padding-top: 60px;\n        padding-bottom: 80px;\n    }',
    text
)


# 2. Fix the Top Secret button formatting
old_btn = r'<button class="btn btn-success btn-block mt-3" id="btnSaveTotales" style="font-weight:bold; font-size:1\.1rem; padding:10px;">💾 Guardar Predicciones</button>'
new_btn = r'<button type="button" id="btnSaveTotales" style="width:100%; padding: 14px; border-radius: 12px; font-weight: 900; border: none; background: var(--secondary-color); color: #000; cursor:pointer; font-size:1.1rem; transition: all 0.2s; margin-top:10px; margin-bottom:10px; box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);">💾 Guardar Predicciones</button>'

text = re.sub(old_btn, new_btn, text)

# Just in case they also meant the Cartelera button, I'll upgrade that one too!
old_cartelera_btn = r'<button type="submit" class="btn btn-success btn-block" id="btnSubmit" style="font-weight: bold; font-size: 1\.1rem; padding: 12px;">💾 Guardar Mis Predicciones</button>'
new_cartelera_btn = r'<button type="submit" id="btnSubmit" style="width:100%; padding: 14px; border-radius: 12px; font-weight: 900; border: none; background: var(--secondary-color); color: #000; cursor:pointer; font-size:1.1rem; transition: all 0.2s; margin-top:10px; box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);">💾 Guardar Mis Predicciones</button>'

text = re.sub(old_cartelera_btn, new_cartelera_btn, text)


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated spacing and button styling")
