import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

bad_logic = r"""// --- LOGICA JUGADOR DESTACADO ---.*?// --- FIN LOGICA JUGADOR DESTACADO ---"""

good_logic = """// --- LOGICA JUGADOR DESTACADO ---
                      let destacadoHtml = "";
                      // --- FIN LOGICA JUGADOR DESTACADO ---"""

html = re.sub(bad_logic, good_logic, html, flags=re.DOTALL)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

