import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = [m.start() for m in re.finditer('cargarDatosAntiguos', text)]
for pos in matches:
    print(text[max(0, pos-50):min(len(text), pos+50)])
