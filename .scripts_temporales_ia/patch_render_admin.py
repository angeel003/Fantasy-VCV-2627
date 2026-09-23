import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_render = r"function renderAdminPanel\(equipos\) \{[\s\S]*?document\.getElementById\('adminListaPartidos'\)\.innerHTML = html;\s*\}"

new_render = """function renderAdminPanel(equipos) {
    let html = "";
    let now = new Date().getTime();
    equipos.forEach(eq => {
        let ts = eq.timestamp || Infinity;
        if (now - ts < 48 * 60 * 60 * 1000) {
            html += `
            <div class="admin-match-box">
                <div style="font-weight:bold; margin-bottom:8px; color: #e65100;">${eq.equipo_local} vs ${eq.rival} <span style="color:#666; font-size:0.8rem; font-weight:normal;">(${eq.id_partido})</span></div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                    <div style="display:flex; gap:10px;">
                        <input type="text" id="adm_sets_${eq.id_partido}" class="form-control form-control-sm" placeholder="Sets (3-1)" value="${eq.oficial_sets || ''}">
                        <input type="text" id="adm_parc_${eq.id_partido}" class="form-control form-control-sm" placeholder="Parc (25-20...)" value="${eq.oficial_parciales || ''}">
                    </div>
                    <input type="text" id="adm_stream_${eq.id_partido}" class="form-control form-control-sm" placeholder="Link Streaming YouTube/Twitch" value="${eq.streaming || ''}">
                    <input type="text" id="adm_frase_${eq.id_partido}" class="form-control form-control-sm" placeholder="Frase del Jugador Destacado (opcional)" value="${eq.frase_destacado || ''}">
                </div>
                <button class="btn btn-sm btn-dark mt-2" style="font-weight:bold;" onclick="guardarResultadoAdmin(event, '${eq.id_partido}')">💾 Guardar Todo</button>
            </div>`;
        }
    });
    if (html === "") html = "<div style='color:white; font-size:0.9rem;'>No hay partidos disponibles o han pasado más de 48h.</div>";
    document.getElementById('adminListaPartidos').innerHTML = html;
}"""

if re.search(old_render, html):
    html = re.sub(old_render, new_render, html)
    print("Replaced renderAdminPanel successfully.")
else:
    print("Failed to find renderAdminPanel via regex.")

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

