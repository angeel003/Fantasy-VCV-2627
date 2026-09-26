import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. HTML Replacement
target_html = """<div style="background: var(--bg-card); padding: 10px; border-radius: 8px; margin-top: 12px; font-size: 0.8rem; border: 1px dashed var(--border-color); color: var(--text-muted);">
                <b>Ejemplo de reparto (Si el premio fuesen 5 pts y el límite 5 de error):</b><br>
                • Alejarte 1 punto exacto: +4 pts<br>
                • Alejarte 2 puntos exactos: +3 pts<br>
                • Alejarte 3 puntos exactos: +2 pts<br>
                • Alejarte 4 puntos exactos: +1 pt<br>
                • Alejarte 5 o más puntos: 0 pts
            </div></p>"""

new_html = """<div id="ejemploProporcionalModal" style="background: var(--bg-card); padding: 10px; border-radius: 8px; margin-top: 12px; font-size: 0.8rem; border: 1px dashed var(--border-color); color: var(--text-muted);">
                <!-- Dynamic Content injected via JS -->
            </div></p>"""

if target_html in text:
    text = text.replace(target_html, new_html)
else:
    print("HTML target not found")


# 2. JS Replacement
target_js = """const pExact = document.getElementById('puntosExactosModal');
                const pMargen = document.getElementById('puntosMargenModal');
                if (pExact) pExact.innerText = data.reglas.diff_exacta;
                if (pMargen) pMargen.innerText = data.reglas.max_dist;"""

new_js = """const pExact = document.getElementById('puntosExactosModal');
                const pMargen = document.getElementById('puntosMargenModal');
                if (pExact) pExact.innerText = data.reglas.diff_exacta;
                if (pMargen) pMargen.innerText = data.reglas.max_dist;

                const ejCont = document.getElementById('ejemploProporcionalModal');
                if(ejCont && data.reglas.diff_exacta && data.reglas.max_dist) {
                    let pDE = parseInt(data.reglas.diff_exacta);
                    let mD = parseInt(data.reglas.max_dist);
                    let calcP = (d) => {
                        if(d >= mD) return 0;
                        return Math.round(pDE * ((mD - d) / mD));
                    };
                    
                    let htmlEjemplo = `<b>Reparto actual de puntos:</b><br>`;
                    htmlEjemplo += `• Alejarte 1 punto exacto: +${calcP(1)} pts<br>`;
                    if (mD > 2) htmlEjemplo += `• Alejarte 2 puntos exactos: +${calcP(2)} pts<br>`;
                    if (mD > 3) htmlEjemplo += `• Alejarte 3 puntos exactos: +${calcP(3)} pts<br>`;
                    
                    if (mD > 4) {
                       htmlEjemplo += `• ...<br>`;
                    }
                    htmlEjemplo += `• Alejarte ${mD} o más puntos: 0 pts`;
                    
                    ejCont.innerHTML = htmlEjemplo;
                }"""

if target_js in text:
    text = text.replace(target_js, new_js)
else:
    print("JS target not found")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated v2.html")
