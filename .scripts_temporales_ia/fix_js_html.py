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
                }"""

new_js = """if(listaReglas) {
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
                if (pAprox) pAprox.innerText = data.reglas.diff_5;
"""
if target_js in text:
    text = text.replace(target_js, new_js)
else:
    print("JS Target not found")

target_html = 'Acertar exactamente la diferencia suma <span style="color:var(--text-gold); font-weight:bold;">+<span id="puntosExactosModal">...</span> pts</span> según el excel oficial. Si fallas por un pequeño margen (dentro del límite configurado en el excel), no te vas de vacío, te llevas <span style="color:var(--text-gold); font-weight:bold;">+<span id="puntosAproxModal">...</span> pts</span>.'

new_html = 'Acertar la diferencia exacta te suma <span style="color:var(--secondary-color); font-weight:bold;">+<span id="puntosExactosModal">...</span> pts</span>. Si fallas por un pequeño margen de 5 puntos, no te vas de vacío, te llevas un bonus de <span style="color:var(--secondary-color); font-weight:bold;">+<span id="puntosAproxModal">...</span> pts</span>.'

if target_html in text:
    text = text.replace(target_html, new_html)
else:
    print("HTML Target not found")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Changes applied")
