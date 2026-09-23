const fs = require('fs');
let html = fs.readFileSync('dev.html', 'utf8');

// Fix btnLogout display and location
let oldBtn = `<div class="col-md-12 text-center" style="margin-top: 10px;">
                    <button id="btnLogout" class="btn btn-outline-danger btn-sm" style="border-radius: 20px; font-weight: bold; padding: 5px 15px;">⬅️ Salir / Volver atrás</button>
                </div>`;
html = html.replace(oldBtn, '');

let headerText = `<header>
    <div class="header-content">`;
let headerRep = `<header>
    <button id="btnLogout" style="display:none; position:absolute; left:15px; top:18px; background:transparent; border:none; color:white; font-size:1.4rem; cursor:pointer; padding:0; outline:none; text-shadow:1px 1px 2px rgba(0,0,0,0.5);" title="Cerrar sesión / Volver atrás">⬅️</button>
    <div class="header-content">`;
html = html.replace(headerText, headerRep);

// Fix display:flex
html = html.replace(`document.getElementById('loginSection').style.display = 'block';`, `document.getElementById('loginSection').style.display = 'flex';`);

// Update login / guest logic to show/hide btnLogout
html = html.replace(`document.getElementById('btnReload').style.display = 'none';`, `document.getElementById('btnReload').style.display = 'none';\n    document.getElementById('btnLogout').style.display = 'none';`);

html = html.replace(`document.getElementById('btnReload').style.display = "flex";`, `document.getElementById('btnReload').style.display = "flex";\n            document.getElementById('btnLogout').style.display = "block";`);


// Add streaming link to match card
let oldLocFecha = `\${infoLocFecha}
                            \${infoPabellon}`;
let newLocFecha = `\${infoLocFecha}
                            \${infoPabellon}
                            \${eq.streaming ? \`<a href="\${eq.streaming}" target="_blank" class="btn btn-sm btn-danger" style="font-weight:bold; border-radius:20px; padding:3px 12px; margin-bottom:10px; display:inline-block;">▶️ Ver Streaming Oficial</a>\` : ''}`;
html = html.replace(new RegExp(oldLocFecha.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\$&'), 'g'), newLocFecha);


// Add streaming and frase to admin panel + 48h limit
let oldAdmin = `function renderAdminPanel(equipos) {
    let html = "";
    equipos.forEach(eq => {
        html += \`
        <div class="admin-match-box">
            <div style="font-weight:bold; margin-bottom:8px; color: #e65100;">\${eq.equipo_local} vs \${eq.rival} <span style="color:#666; font-size:0.8rem; font-weight:normal;">(\${eq.id_partido})</span></div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="adm_sets_\${eq.id_partido}" class="form-control form-control-sm" placeholder="Sets (3-1)" value="\${eq.oficial_sets}">
                <input type="text" id="adm_parc_\${eq.id_partido}" class="form-control form-control-sm" placeholder="Parc (25-20,25-23...)" value="\${eq.oficial_parciales}">
            </div>
            <button class="btn btn-sm btn-dark mt-2" style="font-weight:bold;" onclick="guardarResultadoAdmin(event, '\${eq.id_partido}')">💾 Subir Resultado</button>
        </div>\`;
    });
    if (html === "") html = "<div style='color:white; font-size:0.9rem;'>No hay partidos disponibles.</div>";
    document.getElementById('adminListaPartidos').innerHTML = html;
}`;

let newAdmin = `function renderAdminPanel(equipos) {
    let html = "";
    let now = new Date().getTime();
    equipos.forEach(eq => {
        let ts = eq.timestamp || Infinity;
        if (now - ts < 48 * 60 * 60 * 1000) {
            html += \`
            <div class="admin-match-box">
                <div style="font-weight:bold; margin-bottom:8px; color: #e65100;">\${eq.equipo_local} vs \${eq.rival} <span style="color:#666; font-size:0.8rem; font-weight:normal;">(\${eq.id_partido})</span></div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                    <div style="display:flex; gap:10px;">
                        <input type="text" id="adm_sets_\${eq.id_partido}" class="form-control form-control-sm" placeholder="Sets (3-1)" value="\${eq.oficial_sets || ''}">
                        <input type="text" id="adm_parc_\${eq.id_partido}" class="form-control form-control-sm" placeholder="Parc (25-20,25-23...)" value="\${eq.oficial_parciales || ''}">
                    </div>
                    <input type="text" id="adm_stream_\${eq.id_partido}" class="form-control form-control-sm" placeholder="Link Streaming YouTube/Twitch" value="\${eq.streaming || ''}">
                    <input type="text" id="adm_frase_\${eq.id_partido}" class="form-control form-control-sm" placeholder="Frase del Jugador Destacado (opcional)" value="\${eq.frase_destacado || ''}">
                </div>
                <button class="btn btn-sm btn-dark mt-2" style="font-weight:bold;" onclick="guardarResultadoAdmin(event, '\${eq.id_partido}')">💾 Guardar Todo</button>
            </div>\`;
        }
    });
    if (html === "") html = "<div style='color:white; font-size:0.9rem;'>No hay partidos disponibles o se han pasado las 48h.</div>";
    document.getElementById('adminListaPartidos').innerHTML = html;
}`;

html = html.replace(oldAdmin, newAdmin);


// Update guardarResultadoAdmin
let oldSaveAdmin = `window.guardarResultadoAdmin = function(e, idPart) {
    e.preventDefault();
    const btn = e.target;
    const sets = document.getElementById(\`adm_sets_\${idPart}\`).value.trim();
    const parc = document.getElementById(\`adm_parc_\${idPart}\`).value.trim();
    
    btn.disabled = true; btn.innerText = "Subiendo...";
    
    fetch(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'save_resultado_admin', usuario: currentUser, password: currentPassword, id_partido: idPart, sets: sets, parciales: parc }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })`;

let newSaveAdmin = `window.guardarResultadoAdmin = function(e, idPart) {
    e.preventDefault();
    const btn = e.target;
    const sets = document.getElementById(\`adm_sets_\${idPart}\`).value.trim();
    const parc = document.getElementById(\`adm_parc_\${idPart}\`).value.trim();
    const stream = document.getElementById(\`adm_stream_\${idPart}\`).value.trim();
    const frase = document.getElementById(\`adm_frase_\${idPart}\`).value.trim();
    
    btn.disabled = true; btn.innerText = "Subiendo...";
    
    fetch(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'save_resultado_admin', usuario: currentUser, password: currentPassword, id_partido: idPart, sets: sets, parciales: parc, streaming: stream, frase: frase }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })`;

html = html.replace(oldSaveAdmin, newSaveAdmin);


fs.writeFileSync('dev.html', html);

