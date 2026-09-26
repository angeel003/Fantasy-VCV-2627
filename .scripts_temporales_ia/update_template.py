import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

html_regex = r'(let htmlPartidos = ``;.*?data\.equipos\.forEach\(eq => \{)(.*?)(let valJornada = String\(eq\.jornada_eq \|\| ""\)\.trim\(\);)'

def repl(m):
    return m.group(1) + m.group(2) + """
                let isPredicted = false;
                let pSets = "", pPts = "", pSig = "";
                let ptsText = "", formStr = "";
                if (prediccionesList[eq.id_partido]) {
                    isPredicted = true;
                    pSets = prediccionesList[eq.id_partido].sets || "";
                    pPts = prediccionesList[eq.id_partido].puntos || "";
                    pSig = prediccionesList[eq.id_partido].signo || "";
                    ptsText = pSig === 'A favor (+)' ? 'a favor' : (pSig === 'En contra (-)' ? 'en contra' : '');
                    formStr = ptsText ? `(+${pPts} pts ${ptsText})` : `(${pPts} pts)`;
                    if(pPts == 0) formStr = `(0 pts)`;
                }
                """ + m.group(3)

text = re.sub(html_regex, repl, text, flags=re.DOTALL)

# Now apply collapsed class
text = text.replace('<div class="vcv-card-v2" id="card-v2-${eq.id_partido}" data-category="${eq.categoria}">', '<div class="vcv-card-v2 ${isPredicted && eq.estado !== \'CERRADO\' ? \'collapsed\' : \'\'}" id="card-v2-${eq.id_partido}" data-category="${eq.categoria}">')

text = text.replace('<div class="summary-v2" id="summary-v2-${eq.id_partido}" style="display:none;">', '<div class="summary-v2" id="summary-v2-${eq.id_partido}" style="${isPredicted && eq.estado !== \'CERRADO\' ? \'display:block;\' : \'display:none;\'}">')

text = text.replace('<div class="summary-text-v2" id="summary-text-${eq.id_partido}"></div>', '<div class="summary-text-v2" id="summary-text-${eq.id_partido}">${isPredicted ? `<span style="font-weight:normal; color:var(--text-muted);">Predicción configurada:</span><br><b style="font-size:1.1rem; color:var(--text-main);">${pSets}</b> <span style="color:var(--primary-color); font-weight:800;">${formStr}</span>` : ""}</div>')

text = text.replace('<div class="inputs-eq" id="inputs_eq_${eq.id_partido}">', '<div class="inputs-eq" id="inputs_eq_${eq.id_partido}" style="${isPredicted && eq.estado !== \'CERRADO\' ? \'display:none;\' : \'display:block;\'}">')

text = text.replace('Guardar Predicción', '${isPredicted ? "Modificar Predicción" : "Guardar Predicción"}')
text = text.replace('background:var(--secondary-color); color:#000; font-weight:800; border:none;', '${isPredicted ? "background:transparent; color:var(--text-muted); font-weight:800; border:1px solid var(--border-color);" : "background:var(--secondary-color); color:#000; font-weight:800; border:none;"}')


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Template updated")
