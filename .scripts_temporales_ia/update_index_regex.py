import sys
import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
text = re.sub(
    r'<li>Acertar la <b>Diferencia aproximada \(5\)</b>: <span style="color:var\(--vcv-rojo\); font-weight:bold;">\+\$\{data\.reglas\.diff_5\} pts</span> extra</li>',
    r'<li>Aproximarse a la diferencia (margen de ${data.reglas.max_dist} pts): <span style="color:var(--vcv-rojo); font-weight:bold;">Bonus proporcional</span></li>',
    text
)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated index.html via regex")
