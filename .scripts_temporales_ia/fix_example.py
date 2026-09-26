import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target_html = 'Acertar la diferencia exacta te suma <span style="color:var(--secondary-color); font-weight:bold;">+<span id="puntosExactosModal">...</span> pts</span> de golpe. Si fallas, el sistema te otorga puntos <b>proporcionales</b>: por cada punto de error que te alejes del resultado real ganarás un poco menos, hasta llegar al límite de <span style="color:var(--secondary-color); font-weight:bold;"><span id="puntosMargenModal">...</span> pts</span> de error, donde ya no ganarías bonus.</p>'

new_html = """Acertar la diferencia exacta te suma <span style="color:var(--secondary-color); font-weight:bold;">+<span id="puntosExactosModal">...</span> pts</span> de golpe. Si fallas, el sistema te otorga puntos <b>proporcionales</b>: por cada punto de error que te alejes del resultado real ganarás un poco menos, hasta llegar al límite de <b><span id="puntosMargenModal">...</span> puntos de error</b>, donde ya no ganarías bonus.
            <div style="background: var(--bg-card); padding: 10px; border-radius: 8px; margin-top: 12px; font-size: 0.8rem; border: 1px dashed var(--border-color); color: var(--text-muted);">
                <b>Ejemplo de reparto (Si el premio fuesen 5 pts y el límite 5 de error):</b><br>
                • Alejarte 1 punto exacto: +4 pts<br>
                • Alejarte 2 puntos exactos: +3 pts<br>
                • Alejarte 3 puntos exactos: +2 pts<br>
                • Alejarte 4 puntos exactos: +1 pt<br>
                • Alejarte 5 o más puntos: 0 pts
            </div></p>"""

if target_html in text:
    text = text.replace(target_html, new_html)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced in v2.html")
else:
    print("Target not found in v2.html")
