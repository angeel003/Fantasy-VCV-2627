import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add CSS for .sign-btn-v2.selected
css_rule = """
    .sign-btn-v2.selected {
      background: var(--secondary-color);
      color: #000;
      border-color: var(--secondary-color);
      box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
      transform: translateY(-2px);
    }
"""
text = text.replace('</style>', css_rule + '</style>')

# 2. Change color of DIFERENCIA DE PUNTOS label
text = text.replace('color: var(--text-muted); font-weight: 800; text-transform: uppercase; display:flex; align-items:center; justify-content:center; gap:5px;">DIFERENCIA DE PUNTOS',
                    'color: var(--text-main); font-weight: 700; text-transform: uppercase; display:flex; align-items:center; justify-content:center; gap:5px; letter-spacing:0.5px;">DIFERENCIA DE PUNTOS')

# 3. Update the guiaModal text exactly as requested
old_guia_2 = '<p style="margin-bottom: 10px;"><b>2. Diferencia de puntos:</b> Es la diferencia total de puntos al final del partido entre ambos equipos (la suma de todos los sets).</p>'
new_guia_2 = """<p style="margin-bottom: 10px;">La <b>diferencia de puntos</b> se calcula como la suma de las diferencias de puntos de todos y cada uno de los sets de un partido.</p>
            <div style="background: var(--bg-card-alt); padding: 10px; border-radius: 8px; border: 1px dashed var(--border-color); margin-bottom: 12px; font-size: 0.85rem;">
                <b>Ejemplo real:</b> Si el VCV juega en casa y el partido termina <i>25-20, 23-25, 25-15, 25-22</i>.<br>
                • Set 1: VCV gana de +5<br>
                • Set 2: VCV pierde de -2<br>
                • Set 3: VCV gana de +10<br>
                • Set 4: VCV gana de +3<br>
                La diferencia total es: <code>5 - 2 + 10 + 3 = 16</code>. Tendrías que escribir <b>16</b> en la casilla numérica y seleccionar el signo a favor del <b>VCV (LOCAL)</b>.
            </div>"""

old_guia_3 = '<p style="margin-bottom: 0;"><b>3. Signo:</b> Indica si la diferencia de puntos será a favor (+) o en contra (-) del equipo <b>LOCAL</b>.</p>'
new_guia_3 = """<p style="margin-bottom: 0;"><b>¿Qué gano con esto?</b> Acertar exactamente la diferencia suma <span style="color:var(--text-gold); font-weight:bold;">+<span id="puntosExactosModal">X</span> pts</span> según el excel oficial. Si fallas por un pequeño margen (hasta 5 puntos de error), no te vas de vacío, te llevas <span style="color:var(--text-gold); font-weight:bold;">+<span id="puntosAproxModal">X</span> pts</span>.</p>"""

text = text.replace(old_guia_2, new_guia_2)
text = text.replace(old_guia_3, new_guia_3)
# Clean up "1. Resultado: Elige el resultado final del partido (ej. 3-1)." so it's just the explanation of points diff as requested ("explica solamente que la diferencia de puntos se calcula...")
text = text.replace('<p style="margin-bottom: 10px;"><b>1. Resultado:</b> Elige el resultado final del partido (ej. 3-1).</p>', '')


# 4. Inject the dynamic points into the modal from the login function
injection = """
                    document.getElementById('listaReglasPuntuacion').innerHTML = `
                        <li>Acertar el <b>Resultado Exacto (Sets)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.sets} pts</span></li>
                        <li>Acertar el <b>Ganador del partido</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.ganador} pts</span></li>
                        <li>Acertar la <b>Diferencia de puntos exacta</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_exacta} pts</span> extra</li>
                        <li>Acertar la <b>Diferencia aproximada (5)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_5} pts</span> extra</li>
                    `;
                    
                    const pExact = document.getElementById('puntosExactosModal');
                    const pAprox = document.getElementById('puntosAproxModal');
                    if(pExact) pExact.innerText = data.reglas.diff_exacta;
                    if(pAprox) pAprox.innerText = data.reglas.diff_5;
"""
old_injection = """
                    document.getElementById('listaReglasPuntuacion').innerHTML = `
                        <li>Acertar el <b>Resultado Exacto (Sets)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.sets} pts</span></li>
                        <li>Acertar el <b>Ganador del partido</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.ganador} pts</span></li>
                        <li>Acertar la <b>Diferencia de puntos exacta</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_exacta} pts</span> extra</li>
                        <li>Acertar la <b>Diferencia aproximada (5)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_5} pts</span> extra</li>
                    `;
"""
text = text.replace(old_injection, injection)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated texts and CSS")
