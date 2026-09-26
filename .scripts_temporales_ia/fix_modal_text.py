import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the text in guiaModal
old_text = 'Si fallas por un pequeño margen (hasta 5 puntos de error), no te vas de vacío, te llevas <span style="color:var(--text-gold); font-weight:bold;">+<span id="puntosAproxModal">X</span> pts</span>.</p>'
new_text = 'Si fallas por un pequeño margen (dentro del límite configurado en el excel), no te vas de vacío, te llevas <span style="color:var(--text-gold); font-weight:bold;">+<span id="puntosAproxModal">...</span> pts</span>.</p>'
text = text.replace(old_text, new_text)

# Also replace the 'X' in puntosExactosModal so it looks like a loading state
text = text.replace('<span id="puntosExactosModal">X</span>', '<span id="puntosExactosModal">...</span>')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Text replaced")
