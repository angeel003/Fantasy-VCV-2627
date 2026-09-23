import re
with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# For guest mode matches
html = html.replace('${infoPabellon}\n                    ${infoAdicional}', '${infoPabellon}\n                    ${eq.streaming ? `<a href="${eq.streaming}" target="_blank" class="btn btn-sm btn-danger" style="font-weight:bold; border-radius:20px; padding:3px 12px; margin-bottom:10px; display:inline-block;">▶️ Ver Streaming Oficial</a>` : \'\'}\n                    ${infoAdicional}')

# For logged in mode matches (ABIERTO and CERRADO)
html = html.replace('${infoPabellon}\n                            <div class="reloj-partido"', '${infoPabellon}\n                            ${eq.streaming ? `<a href="${eq.streaming}" target="_blank" class="btn btn-sm btn-danger" style="font-weight:bold; border-radius:20px; padding:3px 12px; margin-bottom:10px; display:inline-block;">▶️ Ver Streaming Oficial</a>` : \'\'}\n                            <div class="reloj-partido"')

html = html.replace('${infoPabellon}\n                            <small style="color:#6c757d; font-weight:bold;">', '${infoPabellon}\n                            ${eq.streaming ? `<a href="${eq.streaming}" target="_blank" class="btn btn-sm btn-danger" style="font-weight:bold; border-radius:20px; padding:3px 12px; margin-bottom:10px; display:inline-block;">▶️ Ver Streaming Oficial</a>` : \'\'}\n                            <small style="color:#6c757d; font-weight:bold;">')

# For historical matches (if needed) - let's skip for now.

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

