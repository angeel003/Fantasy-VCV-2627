import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

target = 'Próximamente</span></div>`;\n                }'
replacement = 'Próximamente</span>${eq.timestamp ? `<div class="reloj-partido" data-ts="${eq.timestamp}" style="font-size:0.85rem; font-weight:bold; padding:4px 8px; background:#fff3cd; color:#856404; border-radius:4px; display:inline-block; margin-left:10px;">Calculando tiempo...</div>` : ""}</div>`;\n                }'

html = html.replace(target, replacement)

# In case line endings are different:
target2 = 'Próximamente</span></div>`;\r\n                }'
replacement2 = 'Próximamente</span>${eq.timestamp ? `<div class="reloj-partido" data-ts="${eq.timestamp}" style="font-size:0.85rem; font-weight:bold; padding:4px 8px; background:#fff3cd; color:#856404; border-radius:4px; display:inline-block; margin-left:10px;">Calculando tiempo...</div>` : ""}</div>`;\r\n                }'

html = html.replace(target2, replacement2)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print("Injected countdown HTML.")

