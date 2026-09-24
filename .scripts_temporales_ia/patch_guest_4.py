import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove any `if (eq.estado === "CERRADO" || eq.visibilidad === "OCULTAR") esPasado = true;` entirely.
html = re.sub(r'if \(eq\.estado === "CERRADO" \|\| eq\.visibilidad === "OCULTAR"\)\s*esPasado = true;', '', html)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print("Cleaned all CERRADO esPasado overrides.")

