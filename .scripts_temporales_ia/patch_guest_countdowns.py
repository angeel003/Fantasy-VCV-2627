import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Title change
html = html.replace('>Próximos Partidos</h4>', '>Partidos en los próximos 10 días</h4>')

# 2. Add countdown in Guest Mode upcoming matches
# Guest mode else block:
# } else {
#     infoAdicional = `<div style="margin-top:10px;"><span style="background-color:#d4edda; color:#155724; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:0.85rem;">⏳ Próximamente</span></div>`;
# }
guest_upcoming_old = '} else {\n                    infoAdicional = `<div style="margin-top:10px;"><span style="background-color:#d4edda; color:#155724; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:0.85rem;">⏳ Próximamente</span></div>`;\n                }'

guest_upcoming_new = """} else {
                    let relojGuest = eq.timestamp ? `<div class="reloj-partido" data-ts="${eq.timestamp}" style="font-size:0.85rem; font-weight:bold; padding:4px 8px; background:#fff3cd; color:#856404; border-radius:4px; display:inline-block; margin-left:10px;">Calculando tiempo...</div>` : '';
                    infoAdicional = `<div style="margin-top:10px; display:flex; align-items:center; flex-wrap:wrap; gap:5px;"><span style="background-color:#d4edda; color:#155724; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:0.85rem;">⏳ Próximamente</span>${relojGuest}</div>`;
                }"""

# Actually, the string in dev.html has specific whitespace. Let's use regex.
guest_upcoming_pattern = r'\} else \{\s*infoAdicional = `<div style="margin-top:10px;"><span style="background-color:#d4edda; color:#155724; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:0\.85rem;">⏳ Próximamente</span></div>`;\s*\}'

html = re.sub(guest_upcoming_pattern, guest_upcoming_new, html)

# 3. Call iniciarRelojes() after innerHTML injection
guest_inject_old = "document.getElementById('contenedorPartidos').innerHTML = finalHtml;\n            document.getElementById('loginSection').style.display = \"none\";"
guest_inject_new = "document.getElementById('contenedorPartidos').innerHTML = finalHtml;\n            document.getElementById('loginSection').style.display = \"none\";\n            if(typeof iniciarRelojes === 'function') iniciarRelojes();"
html = html.replace(guest_inject_old, guest_inject_new)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print("Patched guest view with countdowns and title.")

