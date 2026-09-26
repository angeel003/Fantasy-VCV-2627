import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target_js = """if(listaReglas) {
                    listaReglas.innerHTML = `
                        <li>Acertar el <b>Resultado Exacto (Sets)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.sets} pts</span></li>
                        <li>Acertar el <b>Ganador del partido</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.ganador} pts</span></li>
                        <li>Acertar la <b>Diferencia de puntos exacta</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_exacta} pts</span> extra</li>
                        <li>Acertar la <b>Diferencia aproximada (5)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_5} pts</span> extra</li>
                    `;
                }
                const pExact = document.getElementById('puntosExactosModal');
                const pAprox = document.getElementById('puntosAproxModal');
                if (pExact) pExact.innerText = data.reglas.diff_exacta;
                if (pAprox) pAprox.innerText = data.reglas.diff_5;"""

new_js = """if(listaReglas) {
                    listaReglas.innerHTML = `
                        <li>Acertar el <b>Resultado Exacto (Sets)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.sets} pts</span></li>
                        <li>Acertar el <b>Ganador del partido</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.ganador} pts</span></li>
                        <li>Acertar la <b>Diferencia de puntos exacta</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_exacta} pts</span> extra</li>
                        <li>Aproximarse a la diferencia (margen de ${data.reglas.max_dist} pts): <span style="color:var(--vcv-rojo); font-weight:bold;">Bonus proporcional</span></li>
                    `;
                }
                const pExact = document.getElementById('puntosExactosModal');
                const pMargen = document.getElementById('puntosMargenModal');
                if (pExact) pExact.innerText = data.reglas.diff_exacta;
                if (pMargen) pMargen.innerText = data.reglas.max_dist;
"""

if target_js in text:
    text = text.replace(target_js, new_js)
else:
    print("JS target not found!")

target_html = 'Acertar la diferencia exacta te suma <span style="color:var(--secondary-color); font-weight:bold;">+<span id="puntosExactosModal">...</span> pts</span>. Si fallas por un pequeño margen de 5 puntos, no te vas de vacío, te llevas un bonus de <span style="color:var(--secondary-color); font-weight:bold;">+<span id="puntosAproxModal">...</span> pts</span>.'

new_html = 'Acertar la diferencia exacta te suma <span style="color:var(--secondary-color); font-weight:bold;">+<span id="puntosExactosModal">...</span> pts</span> de golpe. Si fallas, el sistema te otorga puntos <b>proporcionales</b>: por cada punto de error que te alejes del resultado real ganarás un poco menos, hasta llegar al límite de <span style="color:var(--secondary-color); font-weight:bold;"><span id="puntosMargenModal">...</span> pts</span> de error, donde ya no ganarías bonus.'

if target_html in text:
    text = text.replace(target_html, new_html)
else:
    print("HTML target not found!")


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updates applied")
