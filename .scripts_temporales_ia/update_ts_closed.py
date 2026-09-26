import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the loop to fetch category and adjust layout
old_loop = r"""data\.equipos_totales\.forEach\(eq => \{
                    let ptsActuales = data\.puntos_reales\[eq\] \|\| 0;
                    let misPts = "";
                    let listaOtros = "";"""

new_loop = r"""data.equipos_totales.forEach(eq => {
                    let ptsActuales = data.puntos_reales[eq] || 0;
                    let misPts = "";
                    let listaOtros = "";
                    let categoriaEq = "";
                    let matchEncontrado = data.equipos.find(m => m.equipo_local === eq || m.rival === eq);
                    if (matchEncontrado && matchEncontrado.categoria) {
                        categoriaEq = matchEncontrado.categoria;
                    }"""

text = re.sub(old_loop, new_loop, text)

# 2. Update the card layout to include the category
old_card_layout = r"""<div class="vcv-card-v2" style="margin-bottom:10px; padding: 12px; border-left:4px solid var\(--vcv-dorado\);">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <h4 style="color:var\(--text-main\); margin:0; font-weight:800; font-size:1\.1rem; letter-spacing:-0\.5px;">\$\{eq\}</h4>
                            <span style="background:rgba\(16, 185, 129, 0\.15\); color:#10b981; padding:2px 8px; border-radius:6px; border:1px solid rgba\(16, 185, 129, 0\.3\); font-weight:bold; font-size:0\.75rem;">Llevan: \$\{ptsActuales\} pts</span>
                        </div>"""

new_card_layout = r"""<div class="vcv-card-v2" style="margin-bottom:10px; padding: 12px; border-left:4px solid var(--vcv-dorado);">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
                            <div style="display:flex; flex-direction:column;">
                                <h4 style="color:var(--text-main); margin:0; font-weight:800; font-size:1.1rem; letter-spacing:-0.5px;">${eq}</h4>
                                ${categoriaEq ? `<span style="color:var(--text-muted); font-size:0.7rem; font-weight:700; margin-top:2px; text-transform:uppercase; letter-spacing:0.5px;">${categoriaEq}</span>` : ''}
                            </div>
                            <span style="background:rgba(16, 185, 129, 0.15); color:#10b981; padding:4px 8px; border-radius:6px; border:1px solid rgba(16, 185, 129, 0.3); font-weight:bold; font-size:0.75rem; white-space:nowrap; margin-left:8px;">Llevan: ${ptsActuales} pts</span>
                        </div>"""

text = re.sub(old_card_layout, new_card_layout, text)

# 3. Modify isClosed logic to hide miCajonHTML entirely when closed
old_cajon_closed = r"""if \(isClosed\) \{
                        let textoMiPrediccion = misPts !== "" \? `\$\{misPts\} pts` : "No participaste";
                        miCajonHTML = `
                        <div style="background:var\(--bg-card-alt\); padding:10px; border-radius:10px; border:1px solid var\(--border-color\); margin-bottom:10px; display:flex; align-items:center; justify-content:space-between;">
                            <label style="font-weight:700; color:var\(--text-muted\); font-size:0\.75rem; margin:0; text-transform:uppercase;">Tu predicción:</label>
                            <div style="font-size:1\.1rem; font-weight:900; color:var\(--secondary-color\);">\$\{textoMiPrediccion\}</div>
                        </div>`;
                    \}"""

new_cajon_closed = r"""if (isClosed) {
                        miCajonHTML = ""; // El usuario pidió que al cerrarse solo quede el desplegable
                    }"""

text = re.sub(old_cajon_closed, new_cajon_closed, text)


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Top Secret logic")
