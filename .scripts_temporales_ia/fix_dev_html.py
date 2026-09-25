import re

with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_html = r"""<li>Acertar el <b>Resultado Exacto (Sets)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.sets} pts</span></li>
                        <li>Acertar el <b>Ganador del partido</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.ganador} pts</span></li>
                        <li>Acertar la <b>Diferencia de puntos exacta</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_exacta} pts</span> extra</li>
                        <li>Acercarse a la diferencia (hasta <b>${data.reglas.max_dist} pts</b>): <span style="color:var(--vcv-rojo); font-weight:bold;">% proporcional</span> extra</li>"""

text = re.sub(r'<li>Acertar el <b>Resultado Exacto.*?\+.*?\$\{data\.reglas\.diff_5\} pts.*?</li>', new_html, text, flags=re.DOTALL)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("dev.html fixed!")
