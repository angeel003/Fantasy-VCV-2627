import re

with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_text = r'<li>Acercarse a la diferencia (hasta <b>\$\{data\.reglas\.max_dist\} pts</b>): <span style="color:var\(--vcv-rojo\); font-weight:bold;">% proporcional</span> extra</li>'
new_text = r'<li><b>Aproximarse a la diferencia</b> (margen de error de ${data.reglas.max_dist} pts): <span style="color:var(--vcv-rojo); font-weight:bold;">Puntos proporcionales</span> a tu cercanía</li>'

text = re.sub(old_text, new_text, text)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("dev.html updated")
