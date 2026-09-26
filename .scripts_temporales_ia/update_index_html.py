import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_html = r"""<li>Acertar el <b>Resultado Exacto (Sets)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">\+\$\{data\.reglas\.sets\} pts</span></li>
                        <li>Acertar el <b>Ganador del partido</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">\+\$\{data\.reglas\.ganador\} pts</span></li>
                        <li>Acertar la <b>Diferencia de puntos exacta</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">\+\$\{data\.reglas\.diff_exacta\} pts</span> extra</li>
                        <li>Acertar la <b>Diferencia aproximada \(5\)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">\+\$\{data\.reglas\.diff_5\} pts</span> extra</li>"""

new_html = r"""<li>Acertar el <b>Resultado Exacto (Sets)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.sets} pts</span></li>
                        <li>Acertar el <b>Ganador del partido</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.ganador} pts</span></li>
                        <li>Acertar la <b>Diferencia de puntos exacta</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_exacta} pts</span> extra</li>
                        <li><b>Aproximarse a la diferencia</b> (margen de error de ${data.reglas.max_dist} pts): <span style="color:var(--vcv-rojo); font-weight:bold;">Puntos proporcionales</span> a tu cercanía</li>"""

if re.search(old_html, text):
    text = re.sub(old_html, new_html, text)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("index.html updated successfully!")
else:
    print("Could not find the exact HTML string in index.html.")
