import re

with open('dev.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update btnLogin listener
login_regex = r"(document\.getElementById\('btnLogin'\)\.addEventListener\('click', function\(\) \{)(.*?)(^\}\);)"
# wait, it's multiline.
def replacer_login(match):
    pass # better not use regex for the whole block

# Let's do targeted string replacements.
old_login_fetch = "fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login', usuario: usr, password: pwd }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })"
new_login_fetch = """fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login_auth', usuario: usr, password: pwd }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
    .then(res => res.json())
    .then(dataAuth => {
        if (dataAuth.status !== "success") {
            msgBox.className = "alert-box alert-danger"; msgBox.innerText = dataAuth.message; msgBox.style.display = "block";
            btn.disabled = false; btn.innerText = "Entrar al Fantasy"; return;
        }
        currentUser = usr; currentPassword = pwd;
        document.getElementById('displayJugador').innerHTML = "👤 " + (dataAuth.nombre_real || usr);
        let misInsignias = dataAuth.insignias[usr] || [];
        let insigniasHeaderHtml = ""; let isAdmin = false;
        misInsignias.forEach(b => {
            if (b.type === 'admin') isAdmin = true;
            insigniasHeaderHtml += `<img src="${URL_BADGE_GENERIC}" class="badge-header ${getBadgeCSS(b.type)}" title="${b.text}" onclick="showMobileTooltip(event, '${b.text}')">`;
        });
        document.getElementById('displayBadges').innerHTML = insigniasHeaderHtml;
        if (isAdmin) { document.getElementById('adminPanelWrapper').style.display = "block"; }
        
        msgBox.className = "alert-box alert-success"; msgBox.innerText = "¡Credenciales correctas! Descargando cartelera de partidos..."; msgBox.style.display = "block";
        
        fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'get_data', usuario: usr, password: pwd }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })"""
content = content.replace(old_login_fetch, new_login_fetch)

# Now remove the redundant UI update in the nested fetch
redundant_code = """            let displayNom = data.nombre_real && data.nombre_real !== usr ? `${data.nombre_real} <span style="font-size:0.85rem; color:#666; font-weight:normal; font-family:sans-serif;">(@${usr})</span>` : usr;
            document.getElementById('displayJugador').innerHTML = "👤 " + displayNom;
            
            let misInsignias = data.insignias[usr] || [];
            let insigniasHeaderHtml = ""; let isAdmin = false;
            misInsignias.forEach(b => {
                if (b.type === 'admin') isAdmin = true;
                let cssColorClass = getBadgeCSS(b.type);
                insigniasHeaderHtml += `<img src="${URL_BADGE_GENERIC}" class="badge-header ${cssColorClass}" title="${b.text}" onclick="showMobileTooltip(event, '${b.text}')">`;
            });
            document.getElementById('displayBadges').innerHTML = insigniasHeaderHtml;
            
            if (isAdmin) { document.getElementById('adminPanelWrapper').style.display = "block"; renderAdminPanel(data.equipos); } 
            else { document.getElementById('adminPanelWrapper').style.display = "none"; }"""

fixed_redundant_code = """            if (document.getElementById('adminPanelWrapper').style.display === "block") { renderAdminPanel(data.equipos); }"""
content = content.replace(redundant_code, fixed_redundant_code)

# Close the new fetch inside the old fetch catch/finally
old_finally = """    .catch(err => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error de conexión."; msgBox.style.display = "block"; })
    .finally(() => { 
        btn.innerText = "Entrar al Fantasy"; 
        btn.disabled = false; 
    });"""

new_finally = """    .catch(err => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error de conexión cargando datos."; msgBox.style.display = "block"; })
    .finally(() => { 
        btn.innerText = "Entrar al Fantasy"; 
        btn.disabled = false; 
    });
    })
    .catch(err => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error de conexión."; msgBox.style.display = "block"; btn.innerText = "Entrar al Fantasy"; btn.disabled = false; });"""

content = content.replace(old_finally, new_finally)

# MVP Logic
old_match_render = """                let htmlReloj = "";
                let puntosInfo = "";
                
                if (eq.estado === "ABIERTO" && eq.timestamp) {"""

new_match_render = """                let htmlReloj = "";
                let puntosInfo = "";
                
                // --- LOGICA JUGADOR DESTACADO ---
                let destacadoHtml = "";
                let ts1h = eq.timestamp ? eq.timestamp + (60 * 60 * 1000) : 0;
                let ts24h = eq.timestamp ? eq.timestamp + (24 * 60 * 60 * 1000) : 0;
                
                if (eq.timestamp && nowMs < ts1h) {
                    let d = new Date(ts1h);
                    let h1 = d.getHours().toString().padStart(2, '0'); let m1 = d.getMinutes().toString().padStart(2, '0');
                    destacadoHtml = `<div class="mvp-box"><div style="color:#666; font-size:0.9rem; text-align:center;">⏳ La votación del <b>Jugador Destacado</b> se abrirá a las ${h1}:${m1}</div></div>`;
                } else if (eq.timestamp && nowMs >= ts1h && nowMs < ts24h && eq.plantilla && eq.plantilla.length > 0) {
                    if (eq.votos_data && eq.votos_data.my_voto) {
                        let resultsArray = Object.keys(eq.votos_data.votos).map(j => { return { nombre: j, votos: eq.votos_data.votos[j] }; });
                        resultsArray.sort((a,b) => b.votos - a.votos);
                        let barras = resultsArray.map(res => {
                            let pct = Math.round((res.votos / eq.votos_data.total) * 100);
                            let highlight = (res.nombre === eq.votos_data.my_voto) ? 'box-shadow: 0 0 5px var(--vcv-dorado); border: 1px solid var(--vcv-dorado);' : '';
                            return `<div class="mvp-bar-bg" style="${highlight}"><div class="mvp-bar-fill" style="width: ${pct}%;"></div><div class="mvp-bar-text">${res.nombre} ${res.nombre === eq.votos_data.my_voto ? '(Tú)' : ''}</div><div class="mvp-bar-pct">${pct}%</div></div>`;
                        }).join("");
                        destacadoHtml = `<div class="mvp-box"><div class="mvp-title">📊 Resultados Jugador Destacado</div>${barras}</div>`;
                    } else {
                        let opciones = `<option value="">Selecciona un jugador...</option>` + eq.plantilla.map(j => `<option value="${j}">${j}</option>`).join("");
                        destacadoHtml = `<div class="mvp-box" style="border-color: var(--vcv-dorado); background: #fffdf5;"><div class="mvp-title">⭐ ¡Vota al Jugador Destacado!</div><div style="display:flex; gap:10px;"><select class="form-control" id="sel_destacado_${eq.id_partido}">${opciones}</select><button class="btn btn-primary" style="font-weight:bold; white-space:nowrap;" onclick="votarDestacado(event, '${eq.id_partido}')">Votar</button></div></div>`;
                    }
                } else if (eq.timestamp && nowMs >= ts24h && eq.votos_data && eq.votos_data.total > 0) {
                    let resultsArray = Object.keys(eq.votos_data.votos).map(j => { return { nombre: j, votos: eq.votos_data.votos[j] }; });
                    resultsArray.sort((a,b) => b.votos - a.votos);
                    let ganador = resultsArray[0];
                    let pct = Math.round((ganador.votos / eq.votos_data.total) * 100);
                    let fraseHtml = eq.frase_destacado ? `<div class="mvp-quote">${eq.frase_destacado}</div>` : "";
                    
                    let photoUrl = `files/jugadores/${ganador.nombre.replace(/ /g, '_')}.png`;
                    let photoHtml = `<img src="${photoUrl}" onerror="this.style.display='none'" style="width:60px; height:60px; border-radius:50%; border:2px solid var(--vcv-dorado); background:#fff; margin-bottom:10px; object-fit:cover;">`;
                    
                    destacadoHtml = `<div class="mvp-winner-box"><div style="font-size:0.85rem; color:#f8f9fa; text-transform:uppercase; letter-spacing:1px; margin-bottom:5px;">⭐ Jugador Destacado ⭐</div>${photoHtml}<div style="font-size:1.3rem; font-weight:bold; color:var(--vcv-dorado);">${ganador.nombre}</div><div style="font-size:0.8rem; color:#eee; margin-top:2px;">Elegido con el ${pct}% de los votos</div>${fraseHtml}</div>`;
                }
                // --- FIN LOGICA JUGADOR DESTACADO ---

                if (eq.estado === "ABIERTO" && eq.timestamp) {"""
content = content.replace(old_match_render, new_match_render)

old_html_concat = """                    ${infoLocFecha}
                    ${infoPabellon}
                    ${infoAdicional}
                    ${htmlReloj}
                </div>`;"""

new_html_concat = """                    ${infoLocFecha}
                    ${infoPabellon}
                    ${infoAdicional}
                    ${htmlReloj}
                    ${destacadoHtml}
                </div>`;"""
content = content.replace(old_html_concat, new_html_concat)

css_to_add = """
    /* ESTILOS DEL JUGADOR DESTACADO */
    .mvp-box { background: #fdfbf7; border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin-top: 15px; }
    .mvp-title { font-weight: bold; color: var(--vcv-dorado); font-size: 1.05rem; margin-bottom: 10px; text-shadow: 1px 1px 1px rgba(0,0,0,0.1); }
    .mvp-bar-bg { background: #e9ecef; border-radius: 4px; height: 22px; width: 100%; position: relative; overflow: hidden; margin-bottom: 6px; }
    .mvp-bar-fill { background: linear-gradient(90deg, var(--vcv-morado), #9b59b6); height: 100%; width: 0%; transition: width 0.5s ease; }
    .mvp-bar-text { position: absolute; top: 0; left: 8px; line-height: 22px; font-size: 0.8rem; color: #fff; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.8); z-index: 2; }
    .mvp-bar-pct { position: absolute; top: 0; right: 8px; line-height: 22px; font-size: 0.8rem; color: #333; font-weight: bold; z-index: 2; }
    .mvp-winner-box { background: linear-gradient(135deg, var(--vcv-morado), #5e2e60); color: white; border-radius: 8px; padding: 15px; margin-top: 15px; text-align: center; border: 2px solid var(--vcv-dorado); }
    .mvp-quote { font-style: italic; color: #f1c40f; margin-top: 8px; font-size: 0.95rem; }
    .mvp-quote::before { content: "«"; font-size: 1.2rem; }
    .mvp-quote::after { content: "»"; font-size: 1.2rem; }
"""
content = content.replace('/* ESTILO INTRANET */', css_to_add + '\n    /* ESTILO INTRANET */')

js_votar_func = """
window.votarDestacado = function(e, idPart) {
    e.preventDefault();
    const btn = e.target;
    const sel = document.getElementById(`sel_destacado_${idPart}`);
    if(!sel || !sel.value) { alert("Selecciona un jugador primero."); return; }
    
    btn.disabled = true; btn.innerText = "Votando...";
    fetch(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'vote_destacado', usuario: currentUser, password: currentPassword, id_partido: idPart, jugador: sel.value }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })
    .then(res => res.json())
    .then(d => {
        if(d.status === "success") {
            mostrarToast("⭐ ¡Voto registrado!");
            document.getElementById('btnReload').click();
        } else { alert("Error: " + d.message); btn.disabled = false; btn.innerText = "Votar"; }
    })
    .catch(() => { alert("Error de conexión."); btn.disabled = false; btn.innerText = "Votar"; });
}
"""
content = content.replace('function formatFecha(ts) {', js_votar_func + '\nfunction formatFecha(ts) {')

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('dev.html updated successfully with fixed braces')

