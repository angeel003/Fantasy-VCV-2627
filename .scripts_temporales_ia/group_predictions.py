import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_logic = r"""porrasEq\.forEach\(porra => \{
                        if \(porra\.usuario === usr\) misPts = porra\.puntos;
                        listaOtros \+= `
                        <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid var\(--border-color\); color:var\(--text-main\);">
                            <span>👤 \$\{porra\.nombre\}</span>
                            <span style="font-weight:bold; color:var\(--vcv-morado\);">\$\{porra\.puntos\} pts</span>
                        </div>`;
                    \}\);

                    if \(listaOtros === ""\) \{ listaOtros = "<div style='color:#999; font-size:0\.9rem; margin-top:10px;'>Nadie ha hecho su predicción todavía\.</div>"; \}"""

new_logic = r"""let agrupados = {};
                    porrasEq.forEach(porra => {
                        if (porra.usuario === usr) misPts = porra.puntos;
                        if (!agrupados[porra.puntos]) agrupados[porra.puntos] = [];
                        agrupados[porra.puntos].push(porra.nombre);
                    });
                    
                    let sortedPts = Object.keys(agrupados).map(Number).sort((a, b) => b - a);
                    sortedPts.forEach(pts => {
                        let nombresStr = agrupados[pts].map(n => `👤 ${n}`).join(', ');
                        listaOtros += `
                        <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid var(--border-color); gap:12px;">
                            <div style="font-weight:900; color:var(--secondary-color); font-size:1.1rem; white-space:nowrap;">${pts} pts</div>
                            <div style="color:var(--text-muted); font-size:0.75rem; line-height:1.4; text-align:right;">${nombresStr}</div>
                        </div>`;
                    });

                    if (listaOtros === "") { listaOtros = "<div style='color:var(--text-muted); font-size:0.85rem; padding:10px 0;'>Nadie ha hecho su predicción todavía.</div>"; }"""

if re.search(old_logic, text):
    text = re.sub(old_logic, new_logic, text)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully replaced logic")
else:
    print("Logic not found. Using alternative exact search.")
    idx = text.find('porrasEq.forEach(porra => {')
    if idx != -1:
        end_idx = text.find('if (listaOtros === "") {', idx)
        end_idx = text.find('}', end_idx) + 1
        
        chunk = text[idx:end_idx]
        text = text.replace(chunk, new_logic)
        with open('v2.html', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Replaced logic with manual substring")
